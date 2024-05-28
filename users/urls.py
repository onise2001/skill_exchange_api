from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from .views import SignUpView


urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name="login/signup"),
    path('refresh/', TokenRefreshView.as_view()),
]
