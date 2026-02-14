from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from django.db.models import Q

@login_required
def note_list(request):
    query = request.GET.get('q')
    notes = Note.objects.all().order_by('-created_at')
    
    if query:
        notes = notes.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(subject__icontains=query)
        )
        
    return render(request, 'notes/note_list.html', {'notes': notes, 'query': query})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/create_note.html', {'form': form})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})
