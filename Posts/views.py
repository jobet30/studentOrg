from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .forms import PostForm, CommentForm
from .serializers import PostSerializer, CommentSerializer

@login_required
def view_feed(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return render(request, 'posts/feed.html', {'posts': posts})

@login_required
def view_post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'GET':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            post_serializer = PostSerializer(post)
            comments_serializer = CommentSerializer(post.comments.all(), many=True)
            return Response({
                'post': post_serializer.data,
                'comments': comments_serializer.data
            }, status=status.HTTP_200_OK)
        return render(request, 'posts/post_detail.html', {'post': post})

    elif request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return Response({'status': 'success', 'message': 'Comment added successfully.'}, status=status.HTTP_201_CREATED)
            messages.success(request, 'Comment added successfully.')
            return redirect('posts:view_post_detail', post_id=post_id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return Response({'status': 'error', 'errors': comment_form.errors}, status=status.HTTP_400_BAD_REQUEST)
            messages.error(request, 'Error adding comment.')
    return render(request, 'posts/post_detail.html', {'post': post})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            messages.success(request, 'Post created successfully.')
            return redirect('posts:view_feed')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return Response({'status': 'error', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
            messages.error(request, 'Error creating post.')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return Response({'status': 'error', 'message': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            messages.success(request, 'Post updated successfully.')
            return redirect('posts:view_post_detail', post_id=post.id)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return Response({'status': 'error', 'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
            messages.error(request, 'Error updating post.')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})