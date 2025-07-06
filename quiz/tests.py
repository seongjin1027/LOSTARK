from django.test import TestCase
from .models import QuizResult

class QuizResultModelTest(TestCase):
    def test_create_result(self):
        result = QuizResult.objects.create(score=42)
        self.assertEqual(result.score, 42)
        self.assertIsNotNone(result.submitted_at)
