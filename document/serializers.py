# author xiaogang
from rest_framework import serializers
from document.models import *

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'  # 或列出你需要的字段
        read_only_fields = ['author', 'timestamp', 'comment_num', 'vc']

    def get_author(self, obj):
        request = self.context.get('request')
        avatar_url = obj.author.avatar.url if obj.author and obj.author.avatar else ""
        if request and avatar_url:
            avatar_url = request.build_absolute_uri(avatar_url)
        return {
            "name": obj.author.username if obj.author else "匿名",
            "avatar": obj.author.avatar_url,
        }




class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.CharField(source='user.avatar_url', default='')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_avatar','user_name', 'article', 'content', 'reply', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user_name']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        avatar_url = rep.get('user_avatar', '')
        if avatar_url.startswith('http://') or avatar_url.startswith('https://'):
            rep['user_avatar'] = avatar_url.replace(self.context['request'].build_absolute_uri('/media/'), '')
        return rep

