from django import forms
from .models import StudyGroup

class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'description', 'subject', 'preferred_learning_style', 'difficulty_level']
