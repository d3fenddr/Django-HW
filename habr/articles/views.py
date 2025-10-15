from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ArticleForm
from .models import Article, Category, Reaction


def article_list(request):
    qs = Article.objects.select_related('author', 'category')
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
    article = get_object_or_404(Article.objects.select_related('author', 'category'), slug=slug)
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
            art.save()
            return redirect(art.get_absolute_url())
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form})


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
