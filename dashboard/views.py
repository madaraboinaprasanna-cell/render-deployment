from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from groups.models import StudyGroup
from learning.models import UserProgress

@login_required
def dashboard(request):
    user = request.user
    groups = user.study_groups.all()
    progress_count = UserProgress.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'groups': groups,
        'progress_count': progress_count,
        # TODO: Add more analytics like recent activity, upcoming sessions
    }
    return render(request, 'dashboard/dashboard.html', context)
