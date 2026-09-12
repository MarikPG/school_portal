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

    def test_multiple_choices_are_saved_for_one_question(self):
        second_option = ChoiceOption.objects.create(
            question=self.question,
            text='Частково',
            order=2,
        )
        self.question.question_type = Question.QUESTION_TYPE_MULTI
        self.question.save(update_fields=['question_type'])

        response = self.client.post(f'/survey/{self.survey.id}/take/', {
            f'question_{self.question.id}': [self.option.id, second_option.id],
        })

        self.assertRedirects(response, '/survey/complete/')
        saved_response = SurveyResponse.objects.latest('id')
        self.assertEqual(saved_response.answers.count(), 2)

    def test_create_survey_view_saves_questions_and_choices(self):
        response = self.client.post('/survey/create/', {
            'title': 'Нове опитування',
            'description': 'Опис нового опитування',
            'is_active': 'on',
            'questions-TOTAL_FORMS': '2',
            'questions-INITIAL_FORMS': '0',
            'questions-MIN_NUM_FORMS': '0',
            'questions-MAX_NUM_FORMS': '1000',
            'questions-0-text': 'Як вам навчання?',
            'questions-0-question_type': Question.QUESTION_TYPE_MULTI,
            'questions-0-choices': 'Добре\nПотрібно покращити',
            'questions-0-required': 'on',
            'questions-1-text': 'Що змінити?',
            'questions-1-question_type': Question.QUESTION_TYPE_TEXT,
            'questions-1-choices': '',
        })

        created_survey = Survey.objects.get(title='Нове опитування')
        self.assertRedirects(response, '/survey/')
        self.assertEqual(created_survey.questions.count(), 2)
        self.assertEqual(created_survey.questions.first().choices.count(), 2)

    def test_homepage_lists_multiple_active_surveys(self):
        Survey.objects.create(title='Друге опитування', is_active=True)

        response = self.client.get('/survey/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Оцінка навчального процесу')
        self.assertContains(response, 'Друге опитування')
