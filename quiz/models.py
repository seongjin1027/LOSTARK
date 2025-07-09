from django.db import models

class QuizResult(models.Model):
    nickname = models.CharField(max_length=100)  # 닉네임 필드 추가
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname} - Score: {self.score} at {self.submitted_at}"
