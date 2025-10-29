from django.contrib import admin
from .models import Category, Article, Reaction, Rating, Bookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('author', 'category')
    readonly_fields = ('excerpt',)

    actions = ['publish_selected']

    @admin.action(description='Publish selected articles')
    def publish_selected(self, request, queryset):
        queryset.update(status='published')

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'value', 'created_at')
    list_filter = ('value',)
    autocomplete_fields = ('user', 'article')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'score', 'created_at')
    list_filter = ('score',)
    autocomplete_fields = ('user', 'article')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    autocomplete_fields = ('user', 'article')
