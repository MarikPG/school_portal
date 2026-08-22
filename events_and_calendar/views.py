from django.views.generic import ListView
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events_and_calendar/event_list.html'
    context_object_name = 'events'