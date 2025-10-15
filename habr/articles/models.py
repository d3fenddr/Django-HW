from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# Use Cloudinary if available, otherwise local ImageField
try:
    from cloudinary.models import CloudinaryField
    ImageField = CloudinaryField
except Exception:
    from django.db.models import ImageField as ImageField


class Category(models.Model):
    name = models.CharField('Name', max_length=60, unique=True)
    slug = models.SlugField('Slug', max_length=80, unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='articles', verbose_name='Author'
    )
    title = models.CharField('Title', max_length=200)
    slug = models.SlugField('Slug', max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='Category'
    )
    image = ImageField('Image', blank=True, null=True)
    # generated from body; not editable in forms/admin
    excerpt = models.TextField('Excerpt', blank=True, editable=False)
    body = models.TextField('Body')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def save(self, *args, **kwargs):
        # slug
        if not self.slug:
            base = slugify(self.title)[:200] or 'post'
            slug = base
            i = 1
            while Article.objects.filter(slug=slug).exists():
                i += 1
                slug = f'{base}-{i}'
            self.slug = slug

        # always compute excerpt from body (limit)
        limit = 300
        txt = self.body or ''
        self.excerpt = (txt[:limit] + '…') if len(txt) > limit else txt

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:detail', args=[self.slug])

    def likes_count(self):
        return self.reactions.filter(value=1).count()

    def dislikes_count(self):
        return self.reactions.filter(value=-1).count()

    def __str__(self):
        return self.title


class Reaction(models.Model):
    LIKE = 1
    DISLIKE = -1
    VALUES = ((LIKE, 'Like'), (DISLIKE, 'Dislike'))

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='article_reactions', verbose_name='User'
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='reactions', verbose_name='Article'
    )
    value = models.SmallIntegerField('Value', choices=VALUES)
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        unique_together = (('user', 'article'),)
        verbose_name = 'Reaction'
        verbose_name_plural = 'Reactions'

    def __str__(self):
        return f'{self.user} -> {self.article} [{self.value}]'
