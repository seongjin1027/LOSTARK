from django.contrib import admin
from .models import QuizResult

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'score', 'submitted_at')  # ✅ 닉네임 추가
    ordering = ('-submitted_at',)
    search_fields = ('nickname',)  # (선택) 닉네임 검색창 추가
