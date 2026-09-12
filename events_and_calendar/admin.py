from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'location', 'author')
    list_filter = ('start_time', 'author')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_time'