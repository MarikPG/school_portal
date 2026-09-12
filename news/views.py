from django.shortcuts import render, get_object_or_404
from .models import Announcement


def announcement_list(request):
    announcements = Announcement.objects.all()

    return render(request, 'news/announcement_list.html', {
        'announcements': announcements
    })


def announcement_detail(request, id):
    announcement = get_object_or_404(Announcement, pk=id)

    return render(
        request,
        'news/announcement_detail.html',
        {'announcement': announcement}
    )