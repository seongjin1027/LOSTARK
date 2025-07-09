from django.db import models

class QuizResult(models.Model):
    nickname = models.CharField(max_length=100)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname} - Score: {self.score} at {self.submitted_at}"


# ✅ 새로 추가된 모델 (문제별 유저 답안 저장용)
class UserAnswer(models.Model):
    nickname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    question_number = models.IntegerField()
    correct_keywords = models.JSONField()
    user_answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname} - Q{self.question_number}"