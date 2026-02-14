from django.db import models
from django.conf import settings
from groups.models import StudyGroup

class Room(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Video Call Tracking
    video_active = models.BooleanField(default=False)
    video_started_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='started_videos')
    
    # Screen Sharing Tracking
    screen_sharing_active = models.BooleanField(default=False)
    screen_shared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='shared_screens')

    def __str__(self):
        return f"{self.name} - {self.group.name}"

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
