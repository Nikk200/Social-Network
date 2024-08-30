from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSignUpSerializer, UserSignInSerializer, UserSearchSerializer, FriendRequestSerializer, ListFriendsSerializer, PendingRequestSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from api.models import FriendRequest
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta



@api_view()
def test_get(request):
    if isinstance(request.user, AnonymousUser):
        return Response({"message": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"message": "User is logged in", "user": request.user.username}, status=status.HTTP_200_OK)



@api_view(['POST'])
def sign_up_user(request):
    serializer = UserSignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": f'Signup success for {user.email}'}, status = status.HTTP_201_CREATED)
    
    return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def sign_in_user(request):
    serializer = UserSignInSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(username=email.lower(), password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
    return Response({"message": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)




@api_view()
@permission_classes([IsAuthenticated])
def search_user(request):
    keyword = request.GET.get('keyword', '')
    users = User.objects.all()

    if '@' in keyword:
        users = users.filter(email=keyword)
    else:
        users = users.filter(first_name__icontains=keyword) | users.filter(last_name__icontains=keyword) | users.filter(username__icontains=keyword)
    
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_users = paginator.paginate_queryset(users, request)

    serializer = UserSearchSerializer(paginated_users, many=True)

    return paginator.get_paginated_response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    receiver_id = request.data.get('receiver_id')

    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response({"message": "Receiver does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user == receiver:
        return Response({"message": "You cannot send friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
    

    already_friend = FriendRequest.objects.filter(
        (Q(sender=request.user, receiver=receiver, status="accepted")) |
        (Q(sender=receiver, receiver=request.user, status="accepted"))
    )

    if already_friend.exists():
        return Response({"message": "The receiver you are trying to send friend request to is already you friend."}, status=status.HTTP_400_BAD_REQUEST)
    
    existing_friend_req = FriendRequest.objects.filter(
        Q(sender=request.user, receiver=receiver, status='pending') | Q(sender=receiver, receiver=request.user, status='pending')
    ).first()

    if existing_friend_req:
        return Response({"message": "There is already a friend request is pending between you and the receiver"})
    

    one_minute_ago = timezone.now() - timedelta(minutes=1)
    requests_count = FriendRequest.objects.filter(sender=request.user, created_at__gte=one_minute_ago).count()

    if requests_count >= 3:
        return Response({"message": "You cannot send more than 3 requests in a minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    friend_request = FriendRequest.objects.create(sender=request.user, receiver=receiver, status="pending")

    serializer = FriendRequestSerializer(friend_request)

    return Response({"message": "Friend request sent successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user, status='pending')
    except FriendRequest.DoesNotExist:
        return Response({"message": "Friend request does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    friend_request.status = 'accepted'
    friend_request.save()
    serializer = FriendRequestSerializer(friend_request)
    return Response({"message": "Friend request accepted.", "data": serializer.data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user, status='pending')
    except FriendRequest.DoesNotExist:
        return Response({"message": "Friend request does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    friend_request.status = 'rejected'
    friend_request.save()

    serializer = FriendRequestSerializer(friend_request)
    return Response({"message": "Friend request rejected.", "data": serializer.data}, status=status.HTTP_200_OK)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sign_out_user(request):
    logout(request)
    return Response({"message": "User has been logged out."}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    friends = FriendRequest.objects.filter(
        Q(sender=request.user, status='accepted') | Q(receiver=request.user, status='accepted')
    )

    friends_list = []

    if friends:
        for friend in friends:
            if friend.sender == request.user:
                friends_list.append(friend.receiver)
            else:
                friends_list.append(friend.sender)

            serializer = ListFriendsSerializer(friends_list, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "You don't have any friends right now"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    pending_requests = FriendRequest.objects.filter(
        Q(sender=request.user, status='pending') | Q(receiver=request.user, status='pending')
    )

    if pending_requests:
        serializer = PendingRequestSerializer(pending_requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "There are no pending requests exist."}, status=status.HTTP_404_NOT_FOUND)



