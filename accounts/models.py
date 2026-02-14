from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add custom fields here
    bio = models.TextField(max_length=500, blank=True)
    LEARNING_STYLES = [
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('reading', 'Reading/Writing'),
        ('kinesthetic', 'Kinesthetic'),
    ]
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLES, default='visual')
    interests = models.CharField(max_length=255, blank=True, help_text="Comma-separated topics (e.g., Math, Physics, Coding)")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username
