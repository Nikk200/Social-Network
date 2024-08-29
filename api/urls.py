from django.urls import path
from api import views

urlpatterns = [
    path("", views.test_get, name='test'),
    path("sign-up/", views.sign_up_user, name='sign-up'),
    path("sign-in/", views.sign_in_user, name='sign-in'),
]
