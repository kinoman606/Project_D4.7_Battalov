from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from .models import *



class PostList(ListView):
    model = Post
    ordering = '-datePost'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsList(PostList):
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(categoryType='NW')
        return queryset


class ArticleList(ListView):
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(categoryType='AR')
        return queryset
class PostDetail(DetailView):
    model = Post
    template_name = 'news/postdetail.html'
    context_object_name = 'postdetail'


class AuthorList(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'news/authors.html'


class SearchList(ListView):
    model = Post
    ordering = '-datePost'
    context_object_name = 'search'
    template_name = 'news/search_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.categoryType = 'AR'
        return super().form_valid(form)


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType = 'NW'
        return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')





