from django.urls import path
from . import views
from .views import BlogPostListView, BlogPostDetailView, BlogPostFeaturedView, BlogPostCategoryView, PostListView, PostDetailView


urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.index_blog, name="blog"),
    path('blog/category/<category>', views.blog_category, name='category'),
    path('blog/<slug>', views.blog_detail, name="details"),
]