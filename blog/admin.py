from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Article
# Register your models here.

class ArticleModelAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(Article, ArticleModelAdmin)
