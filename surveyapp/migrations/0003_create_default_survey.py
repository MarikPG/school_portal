from django.db import migrations


def create_default_survey(apps, schema_editor):
    Survey = apps.get_model('surveyapp', 'Survey')
    Question = apps.get_model('surveyapp', 'Question')
    ChoiceOption = apps.get_model('surveyapp', 'ChoiceOption')

    survey, created = Survey.objects.get_or_create(
        title='Оцінка навчального процесу',
        defaults={
            'description': 'Поділіться враженнями про навчання в школі.',
            'is_active': True,
        },
    )
    if not created:
        return

    quality_question = Question.objects.create(
        survey=survey,
        text='Наскільки зрозуміло викладачі пояснюють матеріал?',
        question_type='single',
        order=1,
    )
    ChoiceOption.objects.bulk_create([
        ChoiceOption(question=quality_question, text='Дуже зрозуміло', order=1),
        ChoiceOption(question=quality_question, text='Здебільшого зрозуміло', order=2),
        ChoiceOption(question=quality_question, text='Потрібні покращення', order=3),
    ])

    Question.objects.create(
        survey=survey,
        text='Що варто покращити в навчальному процесі?',
        question_type='text',
        order=2,
        required=False,
    )


def remove_default_survey(apps, schema_editor):
    Survey = apps.get_model('surveyapp', 'Survey')
    Survey.objects.filter(title='Оцінка навчального процесу').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('surveyapp', '0002_alter_surveyresponse_user'),
    ]

    operations = [
        migrations.RunPython(create_default_survey, remove_default_survey),
    ]
