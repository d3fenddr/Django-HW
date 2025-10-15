from django.contrib import admin
from .models import Category, Article, Reaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('author', 'category')
    readonly_fields = ('excerpt',)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'value', 'created_at')
    list_filter = ('value',)
    autocomplete_fields = ('user', 'article')
