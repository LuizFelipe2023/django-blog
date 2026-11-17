from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'),
    path('new/', views.news_create, name='news_create'),
    path('<int:id>/', views.news_detail, name='news_detail'),
    path('<int:id>/edit/', views.news_update, name='news_update'),
    path('<int:id>/delete/', views.news_delete, name='news_delete'),
    path('image/<int:image_id>/delete/', views.news_image_delete, name='news_image_delete'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('comment/<int:comment_id>/edit/', views.comment_update, name='comment_update'),
]
