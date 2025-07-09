from django.db import models

class QuizResult(models.Model):
    nickname = models.CharField(max_length=100)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname} - Score: {self.score} at {self.submitted_at}"


class UserAnswer(models.Model):
    nickname = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    question_number = models.IntegerField()
    correct_keywords = models.JSONField()
    user_answer = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname} - Q{self.question_number}"


# ✅ 요약 모델: 유저당 하나의 퀴즈 결과 요약 (IP 포함)
class AnswerSummary(models.Model):
    nickname = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    total_questions = models.IntegerField()
    correct_count = models.IntegerField()
    wrong_count = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname} ({self.ip_address}) - {self.correct_count}/{self.total_questions}"
