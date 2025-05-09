
from rest_framework.viewsets import ModelViewSet
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework import generics, permissions
import os
from rest_framework import status


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all().order_by('-timestamp')
    serializer_class = ArticleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.vc = (instance.vc or 0) + 1
        instance.save(update_fields=['vc'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# views.py


class ArticleCreateView(generics.CreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 打印错误信息
        print("数据验证失败：", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UploadImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.FILES.get('file')
        if not image:
            return Response({'error': 'No file uploaded'}, status=400)

        upload_type = request.query_params.get('type', 'others')  # 例如 ?type=avatar
        # allowed_types = ['avatar', 'article', 'banner', 'others']
        #
        # if upload_type not in allowed_types:
        #     return Response({'error': f'Invalid type: {upload_type}'}, status=400)

        # 确保目录存在
        # save_dir = os.path.join('media', upload_type)
        file_path = default_storage.save(os.path.join(upload_type, image.name), image)

        image_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
        return Response({'url': image_url})


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
