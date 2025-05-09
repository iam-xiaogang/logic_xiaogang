from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_code
from .redis_client import redis_client
from django.conf import settings
from .serializers import PhoneLoginSerializer, UserSerializer
from .models import User
from rest_framework.viewsets import GenericViewSet

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import action


class SendCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone')

        if not phone:
            return Response({"message": "手机号不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        code = generate_code()

        # 存入 Redis，有效期 600 秒
        redis_client.setex(f"login_code:{phone}", settings.REDIS_CODE_EXPIRE_SECONDS, code)

        # 模拟发送短信
        print(f"发送验证码 {code} 到手机号 {phone}")

        return Response({"message": "验证码已发送","code":0}, status=status.HTTP_200_OK)

class PhoneLoginView(APIView):
    def post(self, request):
        print(request.data)
        serializer = PhoneLoginSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            code = serializer.validated_data['code']
            print(phone, code)

            # 从 Redis 获取验证码
            redis_key = f"login_code:{phone}"
            stored_code = redis_client.get(redis_key)

            if stored_code and stored_code == code:
                # 验证成功，创建或获取用户
                user, created = User.objects.get_or_create(phone=phone)
                userinfo = {
                    'id': user.id,
                    'address': user.address,
                    'email': user.email,
                    'phone': phone,
                    'username': user.username,
                    'avatar_url': user.avatar_url,
                    'avatar': request.build_absolute_uri(user.avatar.url) if user.avatar else ''
                }
                # 删除 Redis 中的验证码
                redis_client.delete(redis_key)

                # 生成 JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    "userinfo": userinfo,
                    "refresh": str(refresh),
                    "access_token": str(refresh.access_token),
                    "message": "登录成功"
                })

            return Response({"message": "验证码错误或已过期"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(ListModelMixin,
                  UpdateModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='update')
    def update_user_info(self, request):
        """
        当前登录用户更新自己的信息
        POST /users/user/update/
        """
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "信息更新成功",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class TokenRefreshView(APIView):
    permission_classes = [AllowAny]  # 刷新 token 通常不需要登录

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"message": "缺少 refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({
                "access_token": access_token,
                "message": "access_token 刷新成功"
            })
        except TokenError as e:
            return Response({"message": "refresh token 无效或已过期"}, status=status.HTTP_400_BAD_REQUEST)


