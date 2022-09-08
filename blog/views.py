from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DeleteView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import Post, Image, Comment
from .forms import PostForm, ImageForm, NewUserForm, CommentForm
# Create your views here.

class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/redesign/delete.html'
    success_url = reverse_lazy('post_list')
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            raise Http404("You are not allowed to delete this Post")
        return super(DeletePostView, self).dispatch(request, *args, **kwargs)


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, per_page=6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/redesign/post_list.html', {'posts': posts})


def post_detail(request, slug):
    posts = get_object_or_404(Post, slug=slug)
    comments = posts.comments.filter(active=False)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = posts
            new_comment.save()
            return redirect('post_detail', slug=posts.slug)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/redesign/post_detail.html', {'posts': posts,'comments': comments,'new_comment': new_comment,'comment_form': comment_form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/redesign/post_edit.html', {'form': form})

def post_edit(request, slug):
    posts = get_object_or_404(Post, slug=slug)
    if posts.author != request.user:
        raise Http404("You are not allowed to edit this Post")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=posts)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=posts)
    return render(request, 'blog/redesign/post_edit.html', {'form': form})

def user_profile(request):
    return render(request, 'registration/profile.html', {})


def upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            return render(request, 'pictures/upload.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
        return render(request, 'pictures/upload.html', {'form':form})


def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("user_profile")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register":form})
