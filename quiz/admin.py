from django.contrib import admin
from .models import QuizResult, UserAnswer

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'score', 'submitted_at')
    ordering = ('-submitted_at',)
    search_fields = ('nickname',)

# ✅ 유저 개별 답안 확인용 어드민
@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'ip_address', 'question_number', 'user_answer', 'submitted_at')
    list_filter = ('nickname', 'submitted_at')
    search_fields = ('nickname', 'user_answer')