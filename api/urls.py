from django.urls import path
from api import views

urlpatterns = [
    path("", views.test_get, name='test'),
    path("sign-up/", views.sign_up_user, name='sign-up'),
    path("sign-in/", views.sign_in_user, name='sign-in'),
    path("sign-out/", views.sign_out_user, name='sign-out'),
    path("search-user/", views.search_user, name='search-user'),
    path("send-friend-request/", views.send_friend_request, name='send-friend-request'),
    path("accept-friend-request/<int:request_id>", views.accept_friend_request, name='accept-friend-request'),
    path("reject-friend-request/<int:request_id>", views.reject_friend_request, name='reject-friend-request'),
    path("list-friends/", views.list_friends, name='list-friends'),
    path("list-pending-requests/", views.list_pending_requests, name='list-pending-requests'),
]

