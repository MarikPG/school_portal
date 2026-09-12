from django import forms

from .models import MediaItem


class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem

        fields = [
            "title",
            "description",
            "file",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Назва файлу",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Опис...",
                }
            ),

            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": (
                        ".jpg,.jpeg,.png,.gif,.webp,.bmp,.svg,"
                        ".mp4,.webm,.ogg,.mov,.avi,.mkv,.m4v,.wmv"
                    ),
                }
            ),
        }

    def clean_file(self):
        file = self.cleaned_data.get("file")

        # При редагуванні файл можна не змінювати.
        if not file:
            if self.instance and self.instance.pk and self.instance.file:
                return self.instance.file

            raise forms.ValidationError(
                "Вибери файл."
            )

        extension = file.name.lower().split(".")[-1]

        allowed_extensions = {
            "jpg", "jpeg", "png", "gif", "webp", "bmp", "svg",
            "mp4", "webm", "ogg", "mov", "avi", "mkv", "m4v", "wmv",
        }

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Цей тип файлу не підтримується."
            )

        return file