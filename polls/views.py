from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice

def list_views(request):
    questions = Question.objects.all()
    return render(request, 'polls/list.html', {'questions': questions})

def detail_views(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote_views(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Ви не обрали жодного варіанту!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', question_id=question.id)

def results_views(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choices.all()
    
    total_votes = sum(choice.votes for choice in choices)
    
    options = []
    for choice in choices:
        percentage = round((choice.votes / total_votes * 100), 1) if total_votes > 0 else 0
        options.append({
            'text': choice.choice_text,
            'vote_count': choice.votes,
            'percentage': percentage,
        })

    return render(request, 'polls/form.html', {
        'question': question,
        'total_votes': total_votes,
        'options': options,
    })