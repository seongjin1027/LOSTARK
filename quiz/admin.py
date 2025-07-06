from django.contrib import admin
from .models import QuizResult

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'submitted_at')
    ordering = ('-submitted_at',)
