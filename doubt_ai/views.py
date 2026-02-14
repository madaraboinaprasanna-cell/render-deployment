from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings
from .models import DoubtHistory

API_KEY = settings.GEMINI_API_KEY
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

@login_required
def chat_view(request):
    try:
        history = DoubtHistory.objects.filter(user=request.user).order_by('timestamp')
    except Exception:
        history = []
    return render(request, 'doubt_ai/chat.html', {'history': history})

@login_required
def clear_history(request):
    DoubtHistory.objects.filter(user=request.user).delete()
    return redirect('doubt_ai_chat')

@login_required
def ask_ai(request):
    if not settings.GEMINI_API_KEY:
        return JsonResponse({'error': 'CRITICAL: No API Key found. Please add GEMINI_API_KEY to your .env file.'}, status=500)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            print(f"Doubt AI: User asked: {user_message[:50]}...")
            
            system_instruction = "You are a professional, helpful, and encouraging Academic Tutor. Provide clear, well-structured, and easy-to-understand explanations in perfect English."
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"Instruction: {system_instruction}\n\nStudent Question: {user_message}"}]
                }]
            }
            
            headers = {'Content-Type': 'application/json'}
            
            try:
                # Set a timeout and verify=False as a last resort for local SSL issues
                response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
                print(f"Doubt AI: API Response Status: {response.status_code}")
            except Exception as api_err:
                print(f"Doubt AI: API Request Failed: {str(api_err)}")
                return JsonResponse({'error': f'Network/SSL Error: {str(api_err)}. Please check your internet or if the API key is valid.'}, status=500)
            
            if response.status_code == 200:
                result = response.json()
                try:
                    ai_text = result['candidates'][0]['content']['parts'][0]['text']
                    
                    # Save to history safely
                    try:
                        DoubtHistory.objects.create(
                            user=request.user,
                            message=user_message,
                            response=ai_text
                        )
                    except Exception as db_err:
                        print(f"Doubt AI: DB Save Error: {str(db_err)}")
                        
                    return JsonResponse({'message': ai_text})
                except (KeyError, IndexError) as parse_err:
                    print(f"Doubt AI: Parsing Error: {str(parse_err)}. Response: {result}")
                    return JsonResponse({'error': 'AI responded but in an unexpected format.'}, status=500)
                    
            elif response.status_code == 403:
                err_msg = response.json().get('error', {}).get('message', 'Forbidden')
                print(f"Doubt AI: 403 Forbidden - {err_msg}")
                if "leaked" in err_msg.lower():
                    return JsonResponse({'error': 'CRITICAL: Your Gemini API Key has been BLOCKED (reported as leaked). You MUST get a NEW KEY from Google AI Studio and update your .env file.'}, status=403)
                return JsonResponse({'error': f'API Key Error (403): {err_msg}'}, status=403)
            else:
                print(f"Doubt AI: API Error {response.status_code}: {response.text}")
                return JsonResponse({'error': f'AI API Error {response.status_code}: {response.text[:100]}'}, status=500)
                
        except Exception as e:
            print(f"Doubt AI: Unexpected View Error: {str(e)}")
            return JsonResponse({'error': f'Server Error: {str(e)}'}, status=500)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)
