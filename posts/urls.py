from django.urls import path
from posts.views import ask, post_add

urlpatterns = [
    path('ask/',ask),
    path('post_add/',post_add),
]
