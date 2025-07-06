from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render
import json
from pathlib import Path

from .models import QuizResult

BASE_DIR = Path(__file__).resolve().parent.parent

# 메인 페이지
def index(request):
    return render(request, 'index.html')

# 퀴즈 페이지
def quiz(request):
    return render(request, 'quiz.html')

# 결과 페이지
def result(request):
    return render(request, 'result.html')

# 퀴즈 문제 제공 API
def get_questions(request):
    file_path = BASE_DIR / 'questions' / 'questions.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return JsonResponse(data, safe=False)

# 점수 제출 API
@csrf_exempt
def submit_score(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            score = int(body.get('score', 0))
            result = QuizResult.objects.create(score=score, submitted_at=timezone.now())
            return JsonResponse({'message': '점수 저장 완료', 'id': result.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)

