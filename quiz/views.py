from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render
import json
import os
from pathlib import Path

from .models import QuizResult

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ 닉네임을 세션에 저장하는 API (index.html에서 호출됨)
@csrf_exempt
def store_nickname(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nickname = data.get('nickname')
        request.session['nickname'] = nickname
        return JsonResponse({'message': '닉네임 저장됨'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# 메인 페이지
def index(request):
    return render(request, 'index.html')

# 퀴즈 페이지
def quiz(request):
    return render(request, 'quiz.html')

# 결과 페이지
def result(request):
    nickname = request.session.get('nickname', 'unknown')
    latest = QuizResult.objects.filter(nickname=nickname).order_by('-submitted_at').first()
    return render(request, 'result.html', {'result': latest})

# 퀴즈 문제 제공 API
def get_questions(request):
    with open(os.path.join(BASE_DIR, 'quiz', 'questions.json'), encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)

# 점수 제출 API
@csrf_exempt
def submit_score(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data.get('score', 0)
        nickname = request.session.get('nickname', 'unknown')
        QuizResult.objects.create(nickname=nickname, score=score)
        return JsonResponse({'message': '저장 완료!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


