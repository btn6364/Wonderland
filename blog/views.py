from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Preference
from .forms import CommentCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostLatestView(ListView):
    model = Post
    queryset = Post.objects.all().order_by("-date_posted")[:5]
    template_name = "blog/home.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    # <app>/<model>_<viewtype>.html
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    # <app>/<model>_<viewtype>.html
    model = Post
    fields = ["title", "content"]

    # overide the form_valid to store the author first
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # <app>/<model>_<viewtype>.html
    model = Post
    fields = ["title", "content"]

    # overide the form_valid to store the author first
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"
    # check if this is the author of the post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentCreationForm()
    return render(request, "blog/post_add_comment.html", {"form": form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def post_preference(request, post_id, user_preference):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        obj = ''
        value_obj = ''
        try:
            obj = Preference.objects.get(user=request.user, post=post)
            value_obj = obj.value  # value of user_preference
            value_obj = int(value_obj)
            user_preference = int(user_preference)
            if value_obj != user_preference:
                obj.delete()
                upref = Preference()
                upref.user = request.user
                upref.post = post
                upref.value = user_preference
                if user_preference == 1 and value_obj != 1:
                    post.likes += 1
                    post.dislikes -= 1
                elif user_preference == 2 and value_obj != 2:
                    post.dislikes += 1
                    post.likes -= 1
                upref.save()
                post.save()
                context = {'post': post, 'post_id': post_id}
                return render(request, 'post_detail.html', context)
            elif value_obj == user_preference:
                obj.delete()
                if user_preference == 1:
                    post.likes -= 1
                elif user_preference == 2:
                    post.dislikes -= 1
                post.save()
                context = {'post': post, 'post_id': post_id}
                return render(request, 'post_detail.html', context)
        except Preference.DoesNotExist:
            upref = Preference()
            upref.user = request.user
            upref.post = post
            upref.value = user_preference
            user_preference = int(user_preference)
            if user_preference == 1:
                post.likes += 1
            elif user_preference == 2:
                post.dislikes += 1
            upref.save()
            post.save()
            context = {'post': post, 'post_id': post_id}
            return render(request, 'post_detail.html', context)
    else:
        post = get_object_or_404(Post, id=post_id)
        context = {'post': post, 'post_id': post_id}
        return render(request, 'post_detail.html', context)


def about(request):
    return render(request, "blog/about.html", {"title": "About"})

