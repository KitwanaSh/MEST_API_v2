from django.urls import path
from . import views

urlpatterns = [
    path("schedules/fetch_sch/", views.fetch_class_schedules),
    path("schedules/create/", views.create_class_schedule),
]
