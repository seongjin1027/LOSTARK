from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz.html', views.quiz, name='quiz'),
    path('result.html', views.result, name='result'),
    path('api/questions/', views.get_questions),
    path('api/submit/', views.submit_score),
]
