from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_important = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcements"
    )

    def __str__(self):
        return self.title