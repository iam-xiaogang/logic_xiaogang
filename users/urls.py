"""
URL configuration for hi_logic_xiaogang project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from .views import SendCodeView, PhoneLoginView,UserViewSet,TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
urlpatterns = [
    path('',include(router.urls)),
    path('send_code/', SendCodeView.as_view(), name='send-code'),
    path('login/', PhoneLoginView.as_view(), name='phone-login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

