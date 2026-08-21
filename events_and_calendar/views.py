from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event
from .forms import EventForm

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'

class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

class EventCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('events_and_calendar:event_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('events_and_calendar:event_list')

class EventDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('events_and_calendar:event_list')