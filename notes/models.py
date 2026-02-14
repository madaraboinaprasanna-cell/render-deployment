from django.db import models
from django.conf import settings

class Note(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='notes/', blank=True, null=True)

    def __str__(self):
        return self.title
