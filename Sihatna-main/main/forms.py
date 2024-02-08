from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "forum"]


class SearchForm(forms.Form):
    q = forms.CharField(label='Rechercher', required=False)


class ReplyForm(forms.Form):
    reply = forms.CharField(widget=forms.Textarea)
