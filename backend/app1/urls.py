from . import views
from django.urls import path

urlpatterns = [
    path("info/", views.info, name="info"),
    path("info2/", views.info2, name="info2"),
]