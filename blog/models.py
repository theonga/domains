from django.db import models
from django.urls import reverse
from users.models import  CustomUser
from django.utils.text import slugify

class Article(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(help_text="Post title", blank=False, max_length=255)
    excerpt = models.TextField(help_text="Post excerpt", default="None")
    featured_image = models.ImageField(upload_to='blog/')
    body = models.TextField(help_text="Post body", blank=False)
    published = models.DateTimeField(auto_now=True)

    slug = models.SlugField(max_length=255, default='', blank=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.slug)])
