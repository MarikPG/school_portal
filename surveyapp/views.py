from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import QuestionFormSet, SurveyForm
from .models import Answer, Survey


def home(request):
    surveys = Survey.objects.filter(is_active=True).prefetch_related('questions')
    return render(request, 'surveyapp/home.html', {'surveys': surveys})


def take_survey(request, survey_id):
    survey = get_object_or_404(
        Survey.objects.prefetch_related('questions__choices'),
        id=survey_id,
        is_active=True,
    )

    if request.method == 'POST':
        response = survey.responses.create(
            user=request.user if request.user.is_authenticated else None,
        )
        for question in survey.questions.all():
            if question.question_type == question.QUESTION_TYPE_TEXT:
                text_answer = request.POST.get(f'question_{question.id}', '').strip()
                Answer.objects.create(response=response, question=question, text_answer=text_answer)
                continue

            selected_choices = request.POST.getlist(f'question_{question.id}')
            choices = selected_choices[:1] if question.question_type == question.QUESTION_TYPE_SINGLE else selected_choices
            for choice_id in choices:
                choice = question.choices.filter(id=choice_id).first()
                if choice:
                    Answer.objects.create(response=response, question=question, choice=choice)

        return redirect('survey_complete')

    return render(request, 'surveyapp/take_survey.html', {'survey': survey})


def survey_complete(request):
    return render(request, 'surveyapp/survey_complete.html')


@transaction.atomic
def create_survey(request):
    if request.method == 'POST':
        survey_form = SurveyForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='questions')
        if survey_form.is_valid() and question_formset.is_valid():
            survey = survey_form.save()
            order = 1
            for question_form in question_formset:
                data = question_form.cleaned_data
                if data.get('DELETE'):
                    continue
                question = survey.questions.create(
                    text=data['text'],
                    question_type=data['question_type'],
                    required=data['required'],
                    order=order,
                )
                options = [line.strip() for line in data['choices'].splitlines() if line.strip()]
                question.choices.bulk_create([
                    question.choices.model(question=question, text=option, order=option_order)
                    for option_order, option in enumerate(options, start=1)
                ])
                order += 1
            return redirect('/survey/')
    else:
        survey_form = SurveyForm()
        question_formset = QuestionFormSet(prefix='questions')

    return render(request, 'surveyapp/create_survey.html', {
        'survey_form': survey_form,
        'question_formset': question_formset,
    })
