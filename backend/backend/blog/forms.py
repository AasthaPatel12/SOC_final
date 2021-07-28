from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    comment = forms.CharField()
    class Meta:
        model = Comment
        fields = ['comment']
