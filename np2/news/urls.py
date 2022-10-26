from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('news/', views.PostList.as_view(), name='news'),
    path('news/<int:pk>/', views.PostDetails.as_view(), name='detail'),
    path('news/create/', views.PostCreate.as_view(type='PO'), name='create-post'),
    path('articles/create/', views.PostCreate.as_view(type='AR'),
         name='create-article'),
    path('news/<int:pk>/edit/',
         views.PostUpdate.as_view(type='PO'), name='edit-post'),
    path('articles/<int:pk>/edit/',
         views.PostUpdate.as_view(type='AR'), name='edit-article'),
    path('news/<int:pk>/delete/', views.PostDelete.as_view(), name='delete-post'),
    path('articles/<int:pk>/delete/',
         views.PostDelete.as_view(), name='delete-article'),
    path('search/', views.PostSearch.as_view(), name='search'),
    path('subscribe/<int:category_id>',
         views.subscribe_to_category, name='subscribe'),
]
