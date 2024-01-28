from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

from app.views import *

router = routers.SimpleRouter()

router.register(r"question", QuestionViewset)


urlpatterns =  router.urls + [
    path("user-register/", UserRegisterAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view(), name="token_obtain_pair"),
    path("api/token_refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("theme/list/", ThemeListAPIView.as_view(), name="theme_list"),
    path("theme/create/", ThemeCreateAPIView.as_view(), name="theme_create"),
    
]
