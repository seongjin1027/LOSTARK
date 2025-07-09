from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render
import json
import os
from pathlib import Path

from .models import QuizResult, UserAnswer, AnswerSummary  # ✅ AnswerSummary 추가됨

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ 닉네임을 세션에 저장하는 API
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

        # ✅ IP 주소 추출 (안전 처리 포함)
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR') or '0.0.0.0'

        # ✅ UserAnswer 집계
        user_answers = UserAnswer.objects.filter(nickname=nickname)
        total = user_answers.count()

        wrong = 0
        for ans in user_answers:
            if not any(k.lower() in ans.user_answer.lower() for k in ans.correct_keywords):
                wrong += 1
        correct = total - wrong

        # ✅ AnswerSummary 생성 또는 업데이트
        AnswerSummary.objects.update_or_create(
            nickname=nickname,
            defaults={
                'ip_address': ip,
                'total_questions': total,
                'correct_count': correct,
                'wrong_count': wrong,
            }
        )

        return JsonResponse({'message': '저장 완료!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# ✅ 유저 개별 답안 저장 API
@csrf_exempt
def save_answer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip:
            ip = ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR') or '0.0.0.0'

        UserAnswer.objects.create(
            nickname=request.session.get('nickname', 'unknown'),
            ip_address=ip,
            question_number=data.get('question_number'),
            correct_keywords=data.get('correct_keywords', []),
            user_answer=data.get('user_answer', '')
        )
        return JsonResponse({'status': 'saved'})
    return JsonResponse({'error': 'Invalid request'}, status=400)





