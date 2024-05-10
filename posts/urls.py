from django.urls import path
from posts.views import ask, post_add

urlpatterns = [
    path('ask/',ask,name='ask'),
    path('post_add/',post_add,name='post_add'),
]
