from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models


class MediaItem(models.Model):
    MEDIA_TYPES = (
        ("image", "Фото"),
        ("video", "Відео"),
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Назва"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Опис"
    )

    file = models.FileField(
        upload_to="gallery/",
        verbose_name="Файл"
    )

    # Тип визначається автоматично.
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
        editable=False,
        verbose_name="Тип"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата додавання"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Медіафайл"
        verbose_name_plural = "Медіафайли"

    def __str__(self):
        return self.title

    def determine_media_type(self):
        """
        Визначає тип файлу за його розширенням.
        """
        if not self.file:
            return None

        extension = Path(self.file.name).suffix.lower().lstrip(".")

        image_extensions = {
            "jpg",
            "jpeg",
            "png",
            "gif",
            "webp",
            "bmp",
            "svg",
        }

        video_extensions = {
            "mp4",
            "webm",
            "ogg",
            "mov",
            "avi",
            "mkv",
            "m4v",
            "wmv",
        }

        if extension in image_extensions:
            return "image"

        if extension in video_extensions:
            return "video"

        return None

    def clean(self):
        super().clean()

        if not self.file:
            raise ValidationError({
                "file": "Вибери файл."
            })

        media_type = self.determine_media_type()

        if media_type is None:
            raise ValidationError({
                "file": (
                    "Непідтримуваний тип файлу. "
                    "Дозволені фото: JPG, JPEG, PNG, GIF, WEBP, BMP, SVG. "
                    "Відео: MP4, WEBM, OGG, MOV, AVI, MKV, M4V, WMV."
                )
            })

    def save(self, *args, **kwargs):
        """
        Перед кожним збереженням автоматично визначає тип.
        """
        if self.file:
            detected_type = self.determine_media_type()

            if detected_type:
                self.media_type = detected_type

        self.full_clean()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Видаляє запис з БД і сам файл з диска.
        """
        file = self.file

        result = super().delete(*args, **kwargs)

        if file:
            file.delete(save=False)

        return result