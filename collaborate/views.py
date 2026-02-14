from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from groups.models import StudyGroup
import json

from django.db.models import Q

@login_required
def collaborate_home(request):
    query = request.GET.get('q')
    user_groups = request.user.study_groups.all()
    
    if query:
        user_groups = user_groups.filter(
            Q(name__icontains=query) | 
            Q(subject__icontains=query)
        )
        
    # Find active rooms for these groups
    rooms = []
    for group in user_groups:
        room, created = Room.objects.get_or_create(group=group, defaults={'name': f"{group.name} Room"})
        rooms.append(room)
    return render(request, 'collaborate/home.html', {'rooms': rooms, 'query': query})

@login_required
def room_view(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    if request.user not in group.members.all():
        return redirect('dashboard')
    
    room, created = Room.objects.get_or_create(group=group, defaults={'name': f"{group.name} Room"})
    return render(request, 'collaborate/room.html', {'room': room, 'group': group})

@login_required
def get_messages(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.user not in room.group.members.all():
         return JsonResponse({'error': 'Unauthorized'}, status=403)
         
    last_id = request.GET.get('last_id', 0)
    messages = Message.objects.filter(room=room, id__gt=last_id).order_by('timestamp')
    
    data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%H:%M')
    } for msg in messages]
    
    return JsonResponse({
        'messages': data,
        'video_active': room.video_active,
        'video_started_by': room.video_started_by.username if room.video_started_by else None,
        'screen_active': room.screen_sharing_active,
        'screen_shared_by': room.screen_shared_by.username if room.screen_shared_by else None,
        'peer_id': room.video_started_by.username if room.video_active else (room.screen_shared_by.username if room.screen_sharing_active else None)
    })

@login_required
def send_message(request, room_id):
    if request.method == 'POST':
        room = get_object_or_404(Room, pk=room_id)
        if request.user not in room.group.members.all():
             return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        data = json.loads(request.body)
        content = data.get('content')
        if content:
            msg = Message.objects.create(room=room, sender=request.user, content=content)
            return JsonResponse({'status': 'ok', 'id': msg.id})
            
    return JsonResponse({'error': 'Invaild request'}, status=400)

@login_required
def toggle_video(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.user not in room.group.members.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    if room.video_active:
        room.video_active = False
        room.video_started_by = None
        Message.objects.create(room=room, sender=request.user, content="[System] Video call ended.")
    else:
        room.video_active = True
        room.video_started_by = request.user
        Message.objects.create(room=room, sender=request.user, content="[System] Started a video call. Join now!")
        
    room.save()
    return JsonResponse({'status': 'ok', 'video_active': room.video_active})

@login_required
def toggle_screen(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.user not in room.group.members.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    if room.screen_sharing_active:
        room.screen_sharing_active = False
        room.screen_shared_by = None
        Message.objects.create(room=room, sender=request.user, content="[System] Screen sharing ended.")
    else:
        room.screen_sharing_active = True
        room.screen_shared_by = request.user
        Message.objects.create(room=room, sender=request.user, content="[System] Is now sharing their screen!")
        
    room.save()
    return JsonResponse({'status': 'ok', 'screen_active': room.screen_sharing_active})
