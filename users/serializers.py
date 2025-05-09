# author xiaogang
from rest_framework import serializers
from .models import PhoneLogin
from .models import User
class PhoneLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        # 你可以在这里校验验证码是否正确、是否过期
        return data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'