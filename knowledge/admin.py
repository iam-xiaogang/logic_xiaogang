

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.


def get_all_fields(model):
    return [field.name for field in model._meta.fields]

@admin.register(Article)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Article)
    list_filter = ('category', 'author')
    search_fields = ('title', 'content')


@admin.register(Category)
class KnowledgeCategoryAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Category)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Tag)
class KnowledgeTagAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Tag)

@admin.register(Comment)
class KnowledgeCommentAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Comment)
    search_fields = ('content',)
    list_filter = ('user',)
