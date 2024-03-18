from django.urls import path
from blogpost.apps import BlogpostConfig
from blogpost.views import (
    BlogPostCreateView,
    BlogPostListView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDeleteView
)

app_name = BlogpostConfig.name


urlpatterns = [

    path('new_blogpost/', BlogPostCreateView.as_view(), name='create_blogpost'),
    path('blogpost_list/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blogpost_detail/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blogpost_edit/<int:pk>/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blogpost_del/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]
