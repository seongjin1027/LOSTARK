from django.db import models

class QuizResult(models.Model):
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Score: {self.score} at {self.submitted_at}"
