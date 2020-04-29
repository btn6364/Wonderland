from django.urls import path
from .views import ( PostListView, PostDetailView, 
                     PostCreateView, PostUpdateView, 
                     PostDeleteView, UserPostListView, 
                     PostLatestView, PostLikeToggleRedirect
                   )
from . import views

urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post-delete"),
    path("post/latest/", PostLatestView.as_view(), name="post-latest"),
    path("post/<int:pk>/comment", views.add_comment_to_post, name="post-add-comment"),
    path("post/<int:pk>/like", PostLikeToggleRedirect.as_view(), name="post-like-toggle"),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment-approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment-remove'),
    path("about/", views.about, name="blog-about"),
]




