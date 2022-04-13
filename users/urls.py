from django.urls import path

from users.views import UserRegisterAPIView, UserLoginAPIView, UserLogoutAPIView

app_name = 'users'

urlpatterns = [
    path('', UserRegisterAPIView.as_view(), name="list"),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
]