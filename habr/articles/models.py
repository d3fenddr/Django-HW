from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Avg, Count

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
    STATUS_PENDING = 'pending'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending approval'),
        (STATUS_PUBLISHED, 'Published'),
    )
    status = models.CharField('Status', max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)
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

    @property
    def rating_avg(self):
        result = self.ratings.aggregate(avg=Avg('score'))
        return float(result['avg'] or 0.0)

    @property
    def rating_count(self):
        result = self.ratings.aggregate(cnt=Count('id'))
        return int(result['cnt'] or 0)

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


class Rating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='article_ratings', verbose_name='User'
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='ratings', verbose_name='Article'
    )
    score = models.PositiveSmallIntegerField('Score', choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        unique_together = (('user', 'article'),)
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f'{self.user} rated {self.article} {self.score}'


class Bookmark(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='User'
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='bookmarks', verbose_name='Article'
    )
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        unique_together = (('user', 'article'),)
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'

    def __str__(self):
        return f'{self.user} bookmarked {self.article}'
