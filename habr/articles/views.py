from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .forms import ArticleForm
from .models import Article, Category, Reaction, Rating, Bookmark


def article_list(request):
    qs = Article.objects.select_related('author', 'category')
    # Only published for regular users; staff sees all
    if not request.user.is_staff:
        qs = qs.filter(status=Article.STATUS_PUBLISHED)
    category_slug = request.GET.get('category')
    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    paginator = Paginator(qs, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    categories = Category.objects.all()

    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'categories': categories,
        'active_category': category_slug,
    })


def article_detail(request, slug):
    qs = Article.objects.select_related('author', 'category')
    if not request.user.is_staff:
        qs = qs.filter(models.Q(status=Article.STATUS_PUBLISHED) | models.Q(author=request.user))
    article = get_object_or_404(qs, slug=slug)
    user_reaction = None
    if request.user.is_authenticated:
        user_reaction = Reaction.objects.filter(user=request.user, article=article).first()
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'user_reaction': user_reaction,
    })


@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            art = form.save(commit=False)
            art.author = request.user
            # Non-staff submissions require approval
            if request.user.is_staff:
                art.status = Article.STATUS_PUBLISHED
            else:
                art.status = Article.STATUS_PENDING
            art.save()
            return redirect(art.get_absolute_url())
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form})


@login_required
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not (request.user.is_staff or article.author == request.user):
        return redirect(article.get_absolute_url())
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            art = form.save(commit=False)
            if request.user.is_staff:
                art.status = Article.STATUS_PUBLISHED
            else:
                art.status = Article.STATUS_PENDING
            art.save()
            return redirect(art.get_absolute_url())
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_form.html', {'form': form})


@login_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not (request.user.is_staff or article.author == request.user):
        return redirect(article.get_absolute_url())
    if request.method == 'POST':
        article.delete()
        return redirect('articles:list')
    return render(request, 'articles/article_confirm_delete.html', {'article': article})


@require_POST
@login_required
def react(request, slug):
    article = get_object_or_404(Article, slug=slug)
    value_str = request.POST.get('value')
    value = 1 if value_str == 'like' else -1

    obj, created = Reaction.objects.get_or_create(
        user=request.user, article=article, defaults={'value': value}
    )
    if not created:
        if obj.value == value:
            obj.delete()
        else:
            obj.value = value
            obj.save(update_fields=['value'])
    return redirect(article.get_absolute_url())


@require_POST
@login_required
def rate(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not request.user.is_staff and article.status != Article.STATUS_PUBLISHED and article.author != request.user:
        return redirect(article.get_absolute_url())
    try:
        score = int(request.POST.get('score', ''))
        if score < 1 or score > 5:
            raise ValueError
    except Exception:
        return redirect(article.get_absolute_url())

    obj, _ = Rating.objects.update_or_create(
        user=request.user, article=article, defaults={'score': score}
    )
    return redirect(article.get_absolute_url())


def article_popular(request):
    qs = Article.objects.select_related('author', 'category')
    if not request.user.is_staff:
        qs = qs.filter(status=Article.STATUS_PUBLISHED)
    # filter with average rating >= 4.0
    qs = qs.annotate(avg=models.Avg('ratings__score')).filter(avg__gte=4.0)
    paginator = Paginator(qs, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'categories': Category.objects.all(),
        'active_category': None,
    })


def authors_list(request):
    authors = User.objects.filter(articles__isnull=False).distinct()
    return render(request, 'articles/authors_list.html', {'authors': authors})


def author_detail(request, user_id):
    author = get_object_or_404(User, pk=user_id)
    qs = Article.objects.select_related('author', 'category').filter(author=author)
    if not request.user.is_staff:
        qs = qs.filter(status=Article.STATUS_PUBLISHED)
    return render(request, 'articles/author_detail.html', {
        'author': author,
        'articles': qs,
    })


def categories_index(request):
    cats = Category.objects.all()
    return render(request, 'articles/categories_index.html', {'categories': cats})


@login_required
def bookmarks_list(request):
    qs = Article.objects.select_related('author', 'category').filter(bookmarks__user=request.user)
    return render(request, 'articles/bookmarks.html', {'articles': qs})


@require_POST
@login_required
def toggle_bookmark(request, slug):
    article = get_object_or_404(Article, slug=slug)
    obj, created = Bookmark.objects.get_or_create(user=request.user, article=article)
    if not created:
        obj.delete()
    return redirect(article.get_absolute_url())


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
