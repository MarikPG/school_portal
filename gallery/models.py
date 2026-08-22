from django.db import models
from django.core.exceptions import ValidationError


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

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
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

    def clean(self):
        if not self.file:
            return

        extension = self.file.name.lower().split(".")[-1]

        image_extensions = {
            "jpg",
            "jpeg",
            "png",
            "gif",
            "webp",
        }

        video_extensions = {
            "mp4",
            "webm",
            "ogg",
            "mov",
        }

        if self.media_type == "image" and extension not in image_extensions:
            raise ValidationError(
                "Для типу «Фото» потрібно завантажити зображення."
            )

        if self.media_type == "video" and extension not in video_extensions:
            raise ValidationError(
                "Для типу «Відео» потрібно завантажити відеофайл."
            )