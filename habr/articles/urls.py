from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name='list'),
    path('popular/', views.article_popular, name='popular'),
    path('authors/', views.authors_list, name='authors'),
    path('authors/<int:user_id>/', views.author_detail, name='author_detail'),
    path('categories/', views.categories_index, name='categories'),
    path('bookmarks/', views.bookmarks_list, name='bookmarks'),
    path('signup/', views.signup, name='signup'),
    path('add/', views.article_create, name='create'),
    path('<slug:slug>/', views.article_detail, name='detail'),
    path('<slug:slug>/edit/', views.article_update, name='update'),
    path('<slug:slug>/delete/', views.article_delete, name='delete'),
    path('<slug:slug>/react/', views.react, name='react'),
    path('<slug:slug>/rate/', views.rate, name='rate'),
    path('<slug:slug>/bookmark/', views.toggle_bookmark, name='bookmark'),
]
