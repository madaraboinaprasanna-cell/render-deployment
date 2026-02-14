from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Exam, Question, ExamResult
from groups.models import StudyGroup, UserGroupProgress
from django.conf import settings
from django.contrib import messages
import json
import requests

# Gemini API Config
API_KEY = settings.GEMINI_API_KEY
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

@login_required
def exam_list(request):
    user_groups = request.user.study_groups.all()
    exams = Exam.objects.filter(group__in=user_groups).order_by('-created_at')
    return render(request, 'exams/exam_list.html', {'exams': exams})

@login_required
def test_history(request):
    results = ExamResult.objects.filter(user=request.user).order_by('-completed_at').select_related('exam')
    return render(request, 'exams/test_history.html', {'results': results})

@login_required
def generate_test(request, group_id):
    group = get_object_or_404(StudyGroup, pk=group_id)
    progress, created = UserGroupProgress.objects.get_or_create(user=request.user, group=group)
    schedule_len = len(group.ai_schedule) if group.ai_schedule else 7
    if len(progress.completed_days) < schedule_len:
        messages.error(request, "Access Denied: Complete the 7-day schedule first.")
        return redirect('group_detail', pk=group_id)

    prompt = f"""
    Act as a Senior Academic Examiner. Create a high-quality, 25-question multiple choice test based on: {group.subject}.
    Use professional, clear, and perfectly grammatical English.
    
    For each question, provide:
    1. 'question'
    2. 'options': exactly 4 strings.
    3. 'answer': index 0-3.
    4. 'explanation': Detailed step-by-step analysis in clear English.
    5. 'trick': A clever mnemonic or shortcut to solve it quickly.

    Return ONLY strict JSON:
    [
        {{
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "answer": 0,
            "explanation": "...",
            "trick": "..."
        }},
        ...
    ]
    """
    return actual_generate_logic(request, group, prompt)

def actual_generate_logic(request, group, prompt):
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            raw_text = result['candidates'][0]['content']['parts'][0]['text']
            if "```json" in raw_text: raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text: raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
            questions_data = json.loads(raw_text)
            exam = Exam.objects.create(
                title=f"Weekly Assessment: {group.name}",
                group=group,
                topic=group.subject
            )
            for q_data in questions_data:
                Question.objects.create(
                    exam=exam,
                    text=q_data['question'],
                    option_a=q_data['options'][0],
                    option_b=q_data['options'][1],
                    option_c=q_data['options'][2],
                    option_d=q_data['options'][3],
                    correct_option=chr(65 + q_data['answer']),
                    explanation=q_data.get('explanation', 'Clear analysis provided below.'),
                    trick=q_data.get('trick', 'Review common patterns for this topic.')
                )
            return redirect('take_exam', exam_id=exam.pk)
    except Exception as e:
        messages.error(request, f"AI Generation Failed: {str(e)}")
    return redirect('group_detail', pk=group.pk)

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = exam.questions.all()
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_answers = data.get('answers', {})
            total_time = data.get('total_time', 0)
            
            score = 0
            results_breakdown = []
            
            for q in questions:
                # user_choice is 'A', 'B', 'C', or 'D'
                q_data = user_answers.get(str(q.id), {})
                choice = q_data.get('choice', 'None')
                duration = q_data.get('duration', 0)
                
                is_correct = (choice == q.correct_option)
                if is_correct: score += 1
                
                results_breakdown.append({
                    'text': q.text,
                    'user_choice': choice,
                    'correct_choice': q.correct_option,
                    'is_correct': is_correct,
                    'explanation': q.explanation,
                    'trick': q.trick,
                    'duration': duration,
                    'options': {
                        'A': q.option_a, 'B': q.option_b, 'C': q.option_c, 'D': q.option_d
                    }
                })
            
            ExamResult.objects.create(
                user=request.user,
                exam=exam,
                score=score * 2,
                total_marks=50,
                time_taken=total_time,
                breakdown=results_breakdown
            )
            return JsonResponse({'redirect': f'/exams/result/{exam.id}/'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return render(request, 'exams/take_exam.html', {'exam': exam, 'questions': questions})

@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    # Get the latest result for this user/exam
    result = ExamResult.objects.filter(user=request.user, exam=exam).latest('completed_at')
    return render(request, 'exams/result.html', {'exam': exam, 'result': result})
