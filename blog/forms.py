from django import forms
from .models import Post, Comment

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]