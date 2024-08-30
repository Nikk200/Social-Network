from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class FriendRequest(models.Model):

    STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('accepted', 'ACCEPTED'),
        ('rejected', 'REJECTED')
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"