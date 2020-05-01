from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, RedirectView
from django.db.models import Q
from django.contrib import messages
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = "book_lirary/book_list.html"
    context_object_name = "books"
    ordering = ["title"]

    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            query_list = Book.objects.filter(
                Q(title__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query)
                ).distinct()
        else:
            query_list = Book.objects.all()
        return query_list


class BookDetailView(DetailView):
    # <app>/<model>_<viewtype>.html
    model = Book
    template_name = "book_library/book_detail.html"
    context_object_name = "book"


#view for toggle favorites
class BookFavoriteView(LoginRequiredMixin ,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs["pk"])
        url = book.get_absolute_url()
        user = self.request.user
        if user in book.favorites.all():
            book.favorites.remove(user)
            messages.success(self.request, "Removed from your favorite collection!")
        else:    
            book.favorites.add(user)  
            messages.success(self.request, "Added to your favorite collection!")
        return url


class BookFavoriteListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = "book_lirary/book_list.html"
    context_object_name = "books"
    ordering = ["title"]

    def get_queryset(self):
        user = self.request.user
        query_set = user.book_favorites.all()
        return query_set