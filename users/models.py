from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models

class PhoneLogin(models.Model):
    phone = models.CharField(max_length=15, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("用户必须有手机号")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password or phone)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True, verbose_name="手机号")
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name="用户名")
    email = models.EmailField(blank=True, null=True, verbose_name="邮箱")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="地址")
    role = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name="头像")
    avatar_url = models.CharField(max_length=200,blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []  # 若需要在 createsuperuser 时提示输入其它字段，可加上 'email' 等

    objects = UserManager()

    def __str__(self):
        return self.phone

