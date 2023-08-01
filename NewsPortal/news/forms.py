from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    authorPost = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label='выберите автора', label='Автор')
    postCategory = forms.ModelChoiceField(queryset=Category.objects.all(),empty_label='выберите категорию', label='Категория')
    title = forms.CharField(max_length=255, label='Название')


    class Meta:
        model = Post
        fields = [
            'authorPost',
            'title',
            'textPost',
        ]

    def clean(self):
        cleaned_data = super().clean()
        textPost = cleaned_data.get("textPost")
        title = cleaned_data.get("title")
        if title == textPost:
            raise ValidationError(
                "Текст публикации не должен быть идентичен названию."
            )
        return cleaned_data