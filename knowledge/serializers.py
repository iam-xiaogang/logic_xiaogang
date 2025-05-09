# author xiaogang
from rest_framework import serializers
from .models import Article, Category, Tag, Comment

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

class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(write_only=True, required=False)

    author_name = serializers.CharField(source='author.username', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'author']

    def create(self, validated_data):
        category_name = validated_data.pop('category_name', None)
        if category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category
        return super().create(validated_data)



class CategorySerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name']

class ArticleSimpleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'summary', 'author_name', 'vc']

class CategoryWithArticlesSerializer(serializers.ModelSerializer):
    articles = ArticleSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'articles']
