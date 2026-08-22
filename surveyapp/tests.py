from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Answer, ChoiceOption, Question, Survey, SurveyResponse


class SurveyModelsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='student1',
            email='student1@example.com',
            password='password123',
        )
        self.survey = Survey.objects.create(
            title='Оцінка навчального процесу',
            description='Опитування для студентів',
            is_active=True,
        )
        self.question = Question.objects.create(
            survey=self.survey,
            text='Якісно було пояснено матеріал?',
            question_type=Question.QUESTION_TYPE_SINGLE,
            order=1,
        )
        self.option = ChoiceOption.objects.create(
            question=self.question,
            text='Так',
            order=1,
        )

    def test_survey_and_question_creation(self):
        self.assertEqual(str(self.survey), 'Оцінка навчального процесу')
        self.assertEqual(str(self.question), 'Оцінка навчального процесу: Якісно було пояснено матеріал?')

    def test_response_and_answer_creation(self):
        response = SurveyResponse.objects.create(
            survey=self.survey,
            user=self.user,
        )
        answer = Answer.objects.create(
            response=response,
            question=self.question,
            choice=self.option,
        )

        self.assertEqual(response.answers.count(), 1)
        self.assertEqual(answer.choice, self.option)
        self.assertEqual(answer.question, self.question)

    def test_unique_answer_per_question_in_response(self):
        response = SurveyResponse.objects.create(
            survey=self.survey,
            user=self.user,
        )
        Answer.objects.create(response=response, question=self.question, choice=self.option)

        with self.assertRaises(Exception):
            Answer.objects.create(response=response, question=self.question, choice=self.option)
