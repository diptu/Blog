from django import forms
from .models import Post
class PostForm(forms.Form):
    title   =   forms.CharField()
    class Meta:
        model   = Post
        fields  = [
            "title",
            "content"
        ]
    def __str__(self):
        pass
