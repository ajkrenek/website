from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Image, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'header_image')

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'image')

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','password1','password2')

    def save(self, commit=True):
        user = super(NewUserForm,self).save(commit=False)
        if commit:
            user.save()
        return user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
