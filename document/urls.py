# author xiaogang
# document/urls.py
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet,UploadImageView,ArticleCreateView,CommentListCreateView
from django.urls import path, include

router = DefaultRouter()
router.register(r'articles', ArticleViewSet,)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', UploadImageView.as_view(), name='upload-image'),
    path('create/', ArticleCreateView.as_view(), name='create-article'),
path('comment/', CommentListCreateView.as_view(), name='comment-list-create'),
]
