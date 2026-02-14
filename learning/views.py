from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import LearningPath, Resource, UserProgress

@login_required
def path_list(request):
    paths = LearningPath.objects.all()
    user = request.user
    
    # Recommendation
    recommended = []
    if user.learning_style:
        # Just a simple check if any resource in path matches style would be complex, 
        # let's recommend based on difficulty for now.
        pass

    return render(request, 'learning/path_list.html', {'paths': paths})

@login_required
def path_detail(request, pk):
    path = get_object_or_404(LearningPath, pk=pk)
    resources = path.resources.all()
    completed_resources = UserProgress.objects.filter(user=request.user, resource__in=resources).values_list('resource_id', flat=True)
    
    progress_percent = 0
    if resources.count() > 0:
        progress_percent = int((len(completed_resources) / resources.count()) * 100)

    return render(request, 'learning/path_detail.html', {
        'path': path, 
        'resources': resources,
        'completed_ids': list(completed_resources),
        'progress': progress_percent
    })

@login_required
def complete_resource(request, resource_id):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, pk=resource_id)
        UserProgress.objects.get_or_create(user=request.user, resource=resource)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
