from django.urls import path
from .views import BookListView, BookDetailView, BookFavoriteView, BookFavoriteListView

urlpatterns = [
    path("", BookListView.as_view(), name="library_home"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("<int:pk>/favorite/", BookFavoriteView.as_view(), name="book_favorite"),
    path("favorite/", BookFavoriteListView.as_view(), name="book_favorite_list")
]