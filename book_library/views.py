from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q
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
                )
        else:
            query_list = Book.objects.all()
        return query_list

class BookDetailView(DetailView):
    # <app>/<model>_<viewtype>.html
    model = Book
    template_name = "book_library/book_detail.html"
    context_object_name = "book"

