from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter # To connect the viewset class

router = DefaultRouter()
router.register(r"queries", views.QueryModelView, basename="queries")

urlpatterns = [
    path("", include(router.urls)),
    path("schedules/fetch_sch/", views.fetch_class_schedules),
    path("schedules/create/", views.create_class_schedule),
]

