from django.shortcuts import render

# Create your views here.



from rest_framework import generics, permissions,filters
from rest_framework.permissions import IsAuthenticated
from .models import Article,Category,Comment
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .serializers import ArticleSerializer,CategoryWithArticlesSerializer,CommentSerializer
from rest_framework.generics import ListAPIView

class KnowledgeCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class KnowledgeListView(generics.ListAPIView):
    queryset = Article.objects.all().order_by('-timestamp')
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'category__name', 'tags__name']
    ordering_fields = ['timestamp', 'vc']

class KnowledgeDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'

class KnowledgeUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("你无权修改该文章")
        serializer.save()

# views.py


class KnowledgeDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("你无权删除该文章")
        instance.delete()

from rest_framework.views import APIView

class KnowledgeViewCountIncrease(APIView):
    def post(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            article.vc += 1
            article.save(update_fields=["vc"])
            return Response({"message": "浏览量+1"}, status=200)
        except Article.DoesNotExist:
            return Response({"error": "文章不存在"}, status=404)

class CategoryArticleListView(ListAPIView):
    queryset = Category.objects.filter(visible=True).prefetch_related('articles')
    serializer_class = CategoryWithArticlesSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        article_id = self.request.query_params.get('article')
        if article_id:
            return Comment.objects.filter(article_id=article_id).order_by('-timestamp')
        return Comment.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
