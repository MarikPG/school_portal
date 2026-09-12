from django import forms
from django.forms import BaseFormSet, formset_factory

from .models import Question, Survey


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'is_active']
        labels = {
            'title': 'Назва опитування',
            'description': 'Опис',
            'is_active': 'Опублікувати одразу',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Наприклад: Оцінка навчального процесу'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Коротко поясніть мету опитування'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuestionForm(forms.Form):
    text = forms.CharField(
        label='Текст питання',
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть питання'}),
    )
    question_type = forms.ChoiceField(
        label='Тип відповіді',
        choices=Question.QUESTION_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    choices = forms.CharField(
        label='Варіанти відповіді',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Один варіант у кожному рядку. Для текстового питання залиште порожнім.',
        }),
    )
    required = forms.BooleanField(label='Обов’язкове питання', required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class BaseQuestionFormSet(BaseFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        if not any(
            form.cleaned_data.get('text') and not form.cleaned_data.get('DELETE')
            for form in self.forms
        ):
            raise forms.ValidationError('Додайте хоча б одне питання.')


QuestionFormSet = formset_factory(QuestionForm, formset=BaseQuestionFormSet, extra=1, can_delete=True)
