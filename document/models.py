from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# from users.models import  User
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64, unique=True)
    desp = models.CharField(max_length=300, blank=True)
    tpl_list = models.CharField(max_length=300, blank=True)
    tpl_page = models.CharField(max_length=300, blank=True)
    tpl_mold = models.CharField(max_length=20, choices=[('list', 'List'), ('single_page', 'Single Page')])
    content = models.TextField(blank=True)
    seo_title = models.CharField(max_length=100, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    seo_keywords = models.CharField(max_length=300, blank=True)
    sn = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    icon = models.CharField(max_length=128, default='', blank=True)

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
    name = models.CharField(max_length=64,blank=True)
    editor = models.CharField(max_length=10, default='')
    content = models.TextField()
    content_html = models.TextField(blank=True)
    summary = models.CharField(max_length=300, blank=True)
    thumbnail = models.CharField(max_length=200, blank=True)
    state = models.IntegerField(default=0)
    vc = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='document_articles', on_delete=models.CASCADE, null=True, blank=True,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='articles')
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    h_content = models.CharField(max_length=800, default='')
    h_role = models.IntegerField(default=0)
    art_img = models.ImageField(upload_to='documents', blank=True, null=True, verbose_name="文档图片")
    art_img_url = models.CharField(max_length=200, default='')
    is_crawl = models.IntegerField(default=0)
    origin_url = models.CharField(max_length=200, blank=True)
    origin_author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='document_comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=1024)
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user_id} - {self.article_id} - {self.content[:20]}"


class Recommend(models.Model):
    title = models.CharField(max_length=120)
    img = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    sn = models.IntegerField(default=0)
    state = models.IntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now)


class AccessLog(models.Model):
    ip = models.CharField(max_length=20)
    url = models.CharField(max_length=120)
    timestamp = models.DateTimeField(default=timezone.now)
    remark = models.CharField(max_length=32, blank=True)


class Picture(models.Model):
    name = models.CharField(max_length=64)
    timestamp = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=120)
    remark = models.CharField(max_length=32, blank=True)


class InvitationCode(models.Model):
    code = models.CharField(max_length=64, unique=True)
    user = models.CharField(max_length=64)
    state = models.BooleanField(default=True)


class OnlineTool(models.Model):
    title = models.CharField(max_length=120)
    desp = models.CharField(max_length=120)
    img = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    sn = models.IntegerField(default=0)
    state = models.IntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now)


class Setting(models.Model):
    skey = models.CharField(max_length=64, unique=True)
    svalue = models.CharField(max_length=800, blank=True)


class OrderLog(models.Model):
    notify_time = models.DateTimeField(null=True, blank=True)
    notify_type = models.CharField(max_length=200)
    trade_status = models.CharField(max_length=200)
    out_trade_no = models.CharField(max_length=200)
    buyer_logon_id = models.CharField(max_length=200)
    total_amount = models.CharField(max_length=30)
    subject = models.CharField(max_length=200)
    paystate = models.BooleanField(default=False)
    user_id = models.IntegerField()
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)
    createtime = models.DateTimeField(default=timezone.now)
    callbacktime = models.DateTimeField(null=True, blank=True)


class SpiderInclude(models.Model):
    search_engine = models.CharField(max_length=64, default='')
    num = models.IntegerField(default=0)
    time_label = models.CharField(max_length=20, default='')
    ctime = models.DateTimeField(default=timezone.now)


class FriendlyLink(models.Model):
    link = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    state = models.BooleanField(default=True)
    ctime = models.DateTimeField(default=timezone.now)


class ToolRecord(models.Model):
    types = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    generatortime = models.DateTimeField(default=timezone.now)


class Iprecord(models.Model):
    ip = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    Accessed = models.DateTimeField(default=timezone.now)


class HotSearch(models.Model):
    tag = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)



