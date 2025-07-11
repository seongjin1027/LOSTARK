from django.contrib import admin
from .models import QuizResult, UserAnswer, AnswerSummary


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'score', 'submitted_at')
    ordering = ('-submitted_at',)
    search_fields = ('nickname',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'ip_address', 'question_number', 'user_answer', 'submitted_at')
    list_filter = ('nickname', 'submitted_at')
    search_fields = ('nickname', 'user_answer')


@admin.register(AnswerSummary)
class AnswerSummaryAdmin(admin.ModelAdmin):
    list_display = (
        'nickname', 'ip_address',
        'correct_count', 'wrong_count',
        'total_questions', 'submitted_at'
    )
    ordering = ('-submitted_at',)
    search_fields = ('nickname', 'ip_address')
