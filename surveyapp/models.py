from django.conf import settings
from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPE_SINGLE = 'single'
    QUESTION_TYPE_MULTI = 'multiple'
    QUESTION_TYPE_TEXT = 'text'

    QUESTION_TYPES = [
        (QUESTION_TYPE_SINGLE, 'Один варіант'),
        (QUESTION_TYPE_MULTI, 'Кілька варіантів'),
        (QUESTION_TYPE_TEXT, 'Текстовий відповідь'),
    ]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=QUESTION_TYPE_SINGLE)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['survey', 'order', 'id']
        constraints = [
            models.UniqueConstraint(fields=['survey', 'order'], name='unique_question_order_per_survey')
        ]

    def __str__(self):
        return f'{self.survey}: {self.text}'


class ChoiceOption(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['question', 'order', 'id']
        constraints = [
            models.UniqueConstraint(fields=['question', 'text'], name='unique_choice_text_per_question')
        ]

    def __str__(self):
        return self.text


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, related_name='responses', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='survey_responses', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.user} -> {self.survey}'


class Answer(models.Model):
    response = models.ForeignKey(SurveyResponse, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    choice = models.ForeignKey(ChoiceOption, related_name='answers', on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['response', 'question']
        constraints = [
            models.UniqueConstraint(fields=['response', 'question'], name='unique_answer_per_question_in_response')
        ]

    def __str__(self):
        if self.choice:
            return f'{self.response} -> {self.question}: {self.choice}'
        return f'{self.response} -> {self.question}: {self.text_answer or "No answer"}'
