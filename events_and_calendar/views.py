from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events_and_calendar/event_list.html'
    context_object_name = 'events'
    ordering = ['-start_time']

class EventDetailView(DetailView):
    model = Event
    template_name = 'events_and_calendar/event_detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events_and_calendar/event_form.html'
    fields = ['title', 'description', 'start_time', 'end_time', 'location']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_time'].widget = forms.widgets.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
        form.fields['end_time'].widget = forms.widgets.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)