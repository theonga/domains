from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import  Article
# Create your views here.
class BlogView(ListView):
    model = Article
    template_name = "pages/blog.html"
    context_object_name = "articles"
    paginate_by = 12

class BlogDetailView(DetailView):
    model = Article
    context_object_name = "post"
    template_name = "pages/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
