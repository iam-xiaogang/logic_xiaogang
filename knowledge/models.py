from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    desp = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    visible = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=64, unique=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    content_html = models.TextField(blank=True)
    summary = models.CharField(max_length=300, blank=True)
    state = models.IntegerField(default=0)
    vc = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='knowledge_articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='articles')
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    h_content = models.CharField(max_length=800, default='')
    h_role = models.IntegerField(default=0)
    art_img = models.ImageField(upload_to='documents', blank=True, null=True, verbose_name="文档图片")
    art_img_url = models.CharField(max_length=200, default='')
    origin_url = models.CharField(max_length=200, blank=True)
    origin_author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='knowledge_comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1024)
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_id} - {self.article_id} - {self.content[:20]}"