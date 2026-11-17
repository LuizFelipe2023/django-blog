from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .models import News, NewsImage, Comment
from .forms import NewsForm, CommentForm


def news_home(request):
    news = News.objects.select_related('author').prefetch_related('images').order_by('title')
    return render(request, 'news/news_home.html', {'news': news})


def news_detail(request, id):
    news = get_object_or_404(
        News.objects.select_related('author').prefetch_related('images', 'comments__author'),
        id=id
    )

    if request.method == 'POST':
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '')

        if not request.user.is_authenticated:
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': 'You must be logged in to comment.'}, status=401)
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.author = request.user
            comment.save()

            if is_ajax:
                avatar_url = comment.author.avatar.url if comment.author.avatar else None
                author_name = comment.author.full_name or comment.author.email
                author_initial = author_name[:1].upper()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Comment posted successfully!',
                    'comment': {
                        'id': comment.id,
                        'content': comment.content,
                        'author_name': author_name,
                        'author_avatar': avatar_url,
                        'author_initial': author_initial,
                        'created_at': 'Just now',
                        'can_edit': True,
                        'can_delete': True,
                        'delete_url': reverse('comment_delete', args=[comment.id]),
                        'update_url': reverse('comment_update', args=[comment.id]),
                    },
                    'comments_count': Comment.objects.filter(news=news).count(),
                })
            return redirect('news_detail', id=news.id)
        else:
            if is_ajax:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = CommentForm()

    context = {
        'news': news,
        'comment_form': form,
    }
    return render(request, 'news/news_detail.html', context)


@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()

            for img in form.cleaned_data.get('images', []):
                NewsImage.objects.create(news=news, image=img)
            
            messages.success(request, f'Article "{news.title}" was published successfully!')
            return redirect('news_detail', id=news.id)
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form, 'action': 'Create'})


@login_required
def news_update(request, id):
    news = get_object_or_404(News, id=id)
    if news.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            for img in form.cleaned_data.get('images', []):
                NewsImage.objects.create(news=news, image=img)
            
            messages.success(request, f'Article "{news.title}" was updated successfully!')
            return redirect('news_detail', id=news.id)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/news_form.html', {'form': form, 'news': news, 'action': 'Edit'})


@login_required
def news_delete(request, id):
    news = get_object_or_404(News, id=id)
    if news.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        title = news.title
        news.delete()
        messages.success(request, f'Article "{title}" was deleted successfully.')
        return redirect('news_home')
    return render(request, 'news/news_confirm_delete.html', {'news': news})


@login_required
def news_image_delete(request, image_id):
    image = get_object_or_404(NewsImage, id=image_id)
    if image.news.author != request.user:
        raise PermissionDenied

    news_id = image.news.id
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image was removed successfully.')
    return redirect('news_update', id=news_id)


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '')

    if comment.author != request.user and comment.news.author != request.user:
        if is_ajax:
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
        raise PermissionDenied

    news = comment.news
    news_id = news.id
    if request.method == 'POST':
        comment.delete()
        if is_ajax:
            return JsonResponse({
                'status': 'success',
                'message': 'Comment deleted successfully.',
                'comment_id': comment_id,
                'comments_count': Comment.objects.filter(news=news).count(),
            })
    return redirect('news_detail', id=news_id)


@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('accept', '')

    if comment.author != request.user:
        if is_ajax:
            return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
        raise PermissionDenied

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            if is_ajax:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Comment updated successfully!',
                    'comment': {
                        'id': comment.id,
                        'content': comment.content,
                    }
                })
        else:
            if is_ajax:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return redirect('news_detail', id=comment.news.id)