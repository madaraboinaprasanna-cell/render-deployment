from django.db import models
from django.conf import settings

class Topic(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class LearningPath(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    topics = models.ManyToManyField(Topic, related_name='learning_paths')
    created_at = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(max_length=20, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    
    def __str__(self):
        return self.title

class Resource(models.Model):
    learning_path = models.ManyToManyField(LearningPath, related_name='resources')
    title = models.CharField(max_length=200)
    url = models.URLField()
    RESOURCE_TYPES = [
        ('Video', 'Video'),
        ('Article', 'Article'),
        ('Quiz', 'Quiz'),
    ]
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    
    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'resource')
