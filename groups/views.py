import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import StudyGroup, UserGroupProgress
from .forms import StudyGroupForm
from django.conf import settings
from django.db.models import Q

# Gemini API Config
API_KEY = settings.GEMINI_API_KEY
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

@login_required
def group_list(request):
    query = request.GET.get('q')
    groups = StudyGroup.objects.all().prefetch_related('members')
    
    if query:
        groups = groups.filter(
            Q(name__icontains=query) | 
            Q(subject__icontains=query) | 
            Q(description__icontains=query)
        )
        
    user = request.user
    recommended_groups = []
    if user.interests:
        user_interests = [i.strip().lower() for i in user.interests.split(',')]
        for group in groups:
            if group.subject.lower() in user_interests:
                recommended_groups.append(group)
    return render(request, 'groups/group_list.html', {'groups': groups, 'recommended_groups': recommended_groups, 'query': query})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.members.add(request.user)
            return redirect('group_detail', pk=group.pk)
    else:
        form = StudyGroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def group_detail(request, pk):
    group = get_object_or_404(StudyGroup.objects.prefetch_related('members'), pk=pk)
    is_member = request.user in group.members.all()
    
    if is_member and not group.ai_schedule:
        generate_group_schedule(group)
    
    progress = None
    if is_member:
        progress, created = UserGroupProgress.objects.get_or_create(user=request.user, group=group)

    processed_schedule = []
    completed_count = 0
    total_days = 7
    if group.ai_schedule:
        total_days = len(group.ai_schedule)
        for item in group.ai_schedule:
            day_num = int(item['day'])
            is_done = progress.is_completed(day_num) if progress else False
            can_play = progress.can_unlock(day_num) if progress else False
            
            if is_done: completed_count += 1
            
            processed_item = item.copy()
            processed_item['status'] = 'completed' if is_done else ('unlocked' if can_play else 'locked')
            processed_schedule.append(processed_item)

    # Scoreboard Logic
    progress_percent = int((completed_count / total_days) * 100) if total_days > 0 else 0
    can_take_test = (completed_count >= total_days)

    return render(request, 'groups/group_detail.html', {
        'group': group, 
        'is_member': is_member,
        'schedule': processed_schedule,
        'progress_percent': progress_percent,
        'completed_count': completed_count,
        'total_days': total_days,
        'can_take_test': can_take_test
    })

@login_required
def complete_day(request, pk, day_num):
    group = get_object_or_404(StudyGroup, pk=pk)
    if request.user in group.members.all():
        progress, created = UserGroupProgress.objects.get_or_create(user=request.user, group=group)
        day_num = int(day_num)
        if day_num not in progress.completed_days:
            if progress.can_unlock(day_num):
                progress.completed_days.append(day_num)
                progress.save()
    return redirect('group_detail', pk=pk)

def generate_group_schedule(group):
    prompt = f"""
    Act as a professional Academic Advisor and AI Group Admin for the study group '{group.name}', which is exploring the subject of '{group.subject}'.
    Your goal is to create a high-quality, 7-day learning path that is both rigorous and easy to follow.
    
    For each day, provide:
    1. A clear, academic 'topic' name.
    2. Comprehensive 'daily_notes' written in perfect, encouraging English. These notes should explain the core concepts of the day like a helpful teacher.
    3. An estimated 'time' (e.g., '1 hour 30 mins') that reflects the complexity of the task.
    
    Format the output as a strict JSON list of objects:
    [
        {{
            "day": 1,
            "topic": "Introduction to...",
            "daily_notes": "In today's lesson, we will focus on...",
            "time": "2 hours"
        }},
        ...
    ]
    Ensure the JSON is valid and do not include any conversational filler.
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            # Basic parsing logic same as before
            if "```json" in raw_text: raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            group.ai_schedule = json.loads(raw_text)
            group.save()
    except: pass

@login_required
def join_group(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    if request.user not in group.members.all():
        group.members.add(request.user)
    return redirect('group_detail', pk=pk)
