from django.urls import path
from users.views import *


urlpatterns = [
    path("signup/", signup),
    path("user_login/", user_login)
]
