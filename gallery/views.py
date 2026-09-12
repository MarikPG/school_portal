from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MediaItemForm
from .models import MediaItem


def gallery(request):
    media_items = MediaItem.objects.all()

    return render(
        request,
        "gallery/gallery.html",
        {
            "media_items": media_items,
        },
    )


def upload_media(request):
    if request.method == "POST":
        form = MediaItemForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Файл успішно додано до галереї."
            )

            return redirect("gallery:gallery")

    else:
        form = MediaItemForm()

    return render(
        request,
        "gallery/upload.html",
        {
            "form": form,
            "is_edit": False,
        },
    )


def edit_media(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)

    old_file = item.file

    if request.method == "POST":
        form = MediaItemForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():
            new_file = request.FILES.get("file")

            form.save()

            # Якщо завантажили новий файл —
            # видаляємо старий.
            if new_file and old_file:
                if old_file.name != item.file.name:
                    old_file.delete(save=False)

            messages.success(
                request,
                "Файл успішно відредаговано."
            )

            return redirect("gallery:gallery")

    else:
        form = MediaItemForm(instance=item)

    return render(
        request,
        "gallery/upload.html",
        {
            "form": form,
            "item": item,
            "is_edit": True,
        },
    )


def delete_media(request, pk):
    item = get_object_or_404(MediaItem, pk=pk)

    if request.method == "POST":
        item.delete()

        messages.success(
            request,
            "Файл успішно видалено."
        )

        return redirect("gallery:gallery")

    return render(
        request,
        "gallery/delete.html",
        {
            "item": item,
        },
    )