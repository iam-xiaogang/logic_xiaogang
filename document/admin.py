from django.contrib import admin
from .models import *
# Register your models here.


def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Article)
    list_filter = ('category', 'author')
    search_fields = ('title', 'content')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Category)
    search_fields = ('title',)
    list_filter = ('title',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Tag)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Comment)
    search_fields = ('content','user')
    list_filter = ('user',)
