from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
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
    #<app>/<model>_<viewtype>.html
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    #<app>/<model>_<viewtype>.html
    model = Post
    fields = ["title", "content"]

    #overide the form_valid to store the author first
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    #<app>/<model>_<viewtype>.html
    model = Post
    fields = ["title", "content"]

    #overide the form_valid to store the author first
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
    #check if this is the author of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, "blog/about.html", {"title": "About"})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentCreationForm()
    return render(request, "blog/post_add_comment.html", {"form": form})


# class CommentCreateView(LoginRequiredMixin, CreateView):
#     #<app>/<model>_<viewtype>.html
#     model = Comment
#     fields = ["text"]

#     #overide the form_valid to store the author first
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


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