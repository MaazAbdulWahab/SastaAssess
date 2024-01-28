from django.urls import path
from users.views import *

urlpatterns = [
    path("me/", Me.as_view()),
    path("all/", AllUsers.as_view()),
]
