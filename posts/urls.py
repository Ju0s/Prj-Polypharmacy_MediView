from django.urls import path
from posts.views import ask

urlpatterns = [
    path('ask/',ask),
]
