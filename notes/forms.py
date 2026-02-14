from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'subject', 'content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Share your prepared notes here...'}),
        }
