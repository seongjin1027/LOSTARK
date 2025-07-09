from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.store_nickname, name='store_nickname'),
    path('quiz.html', views.quiz, name='quiz'),
    path('result.html', views.result, name='result'),
    path('api/questions/', views.get_questions),
    path('api/submit/', views.submit_score),
    path('api/save_answer/', views.save_answer),  # ✅ 유저 답변 저장용
]