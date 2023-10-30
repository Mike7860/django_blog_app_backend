from django.shortcuts import render
from .models import Home, About, Profile, Category, Skills, Portfolio, BlogPost, BlogCategories
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from portfolio_app.serializers import BlogPostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.http import HttpResponse
from django.views.generic.list import ListView


def index(request):
    # Home
    home = Home.objects.latest('updated')
    # About
    about = About.objects.latest('updated')
    profiles = Profile.objects.filter(about=about)

    # Skills
    categories = Category.objects.all()

    # Portfolio
    portfolios = Portfolio.objects.all()


    context = {
        'home': home,
        'about': about,
        'profiles': profiles,
        'categories': categories,
        'portfolios': portfolios,
        'num_visits': home.visits_count
    }

    return render(request, 'index.html', context)


def index_blog(request):
    #posts = BlogPost.objects.all().order_by('-date_created')
    categories = [category for category, _ in BlogCategories.choices]

    context_blog = {
        #'posts': posts,
        'categories': categories
    }
    return render(request, 'blog_index.html', context_blog)


class PostListView(ListView):
    model = BlogPost
    context_object_name = 'posts'
    template_name = 'blog_index.html'


class CategoryListView(ListView):
    model = BlogCategories
    context_object_name = 'categories'
    template_name = 'blog_index.html'


class PostDetailView(ListView):
    model = BlogPost
    context_object_name = 'posts'
    template_name = 'blog_details.html'


def blog_detail(request, slug):
    post = BlogPost.objects.get(slug=slug)
    context = {
        "post": post
    }
    return render(request, "blog_details.html", context)


def blog_category(request, category):
    #post = BlogPost.objects.filter(categories__name__contains=category)
    category_posts = BlogPost.objects.order_by('-date_created').filter(category__iexact=category)
    context_category = {
        "category": category,
        "category_posts": category_posts
    }
    return render(request, "blog_category.html", context_category)


#DRF Classes
class BlogPostListView(ListAPIView):
    queryset = BlogPost.objects.order_by('-date_created')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny, )


class BlogPostDetailView(RetrieveAPIView):
    queryset = BlogPost.objects.order_by('-date_created')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny, )


class BlogPostFeaturedView(ListAPIView):
    queryset = BlogPost.objects.all().filter(featured=True)
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny, )


class BlogPostCategoryView(APIView):
    serializer_class = BlogPostSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        category = data['category']
        queryset = BlogPost.objects.order_by('-date_created').filter(category__iexact=category)

        serializer = BlogPostSerializer(queryset, many=True)

        return Response(serializer.data)