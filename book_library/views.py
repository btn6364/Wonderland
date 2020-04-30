from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = "book_lirary/book_list.html"
    context_object_name = "books"
    ordering = ["title"]

class BookDetailView(DetailView):
    # <app>/<model>_<viewtype>.html
    model = Book
    template_name = "book_library/book_detail.html"
    context_object_name = "book"

