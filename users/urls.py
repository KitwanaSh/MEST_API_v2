from django.urls import path
from users.views import *


urlpatterns = [
    path("signup/", signup),
    path("user_login/", user_login),
    path("forgot_password/", ForgotPasswordAPIView.as_view()),
    path("reset_password/", ResetPasswordAPIView.as_view()),
    path("user_profile/", UserProfileAPIView.as_view()),
    path("change_password/", ChangePasswordAPIView.as_view()),
]
