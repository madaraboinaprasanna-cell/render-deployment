from django.db import models
from django.conf import settings
from groups.models import StudyGroup

class Exam(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='exams')
    topic = models.CharField(max_length=255)
    weekly_notes = models.TextField(null=True, blank=True, help_text="AI generated notes for the week")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.group.name}"

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.TextField(null=True, blank=True, help_text="Step-by-step analysis")
    trick = models.TextField(null=True, blank=True, help_text="Trick to solve in less time")

    def __str__(self):
        return self.text[:50]

class ExamResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_marks = models.IntegerField(default=50)
    time_taken = models.IntegerField(default=0, help_text="Time taken in seconds")
    breakdown = models.JSONField(null=True, blank=True, help_text="Per question time and correctness")
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exam.title}: {self.score}"
