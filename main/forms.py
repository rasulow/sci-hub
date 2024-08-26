from django import forms
from . import models

class Article_CommentForm(forms.Form):
    class Meta:
        model = models.Article_comment
        fields = ['comment']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Arcticle
        fields = '__all__'
        exclude = ['user_name']

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    }
                ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
    
                }), 
            }
