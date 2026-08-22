from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import MediaItemForm
from .models import MediaItem


def gallery(request):
    media_items = MediaItem.objects.all()

    return render(
        request,
        'gallery/gallery.html',
        {
            'media_items': media_items,
        },
    )


def upload_media(request):
    if request.method == 'POST':
        form = MediaItemForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Файл успішно додано до галереї.'
            )

            return redirect('gallery:gallery')

    else:
        form = MediaItemForm()

    return render(
        request,
        'gallery/upload.html',
        {
            'form': form,
        },
    )