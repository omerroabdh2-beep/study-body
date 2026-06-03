from django.db import models  # type: ignore[import]
from django.contrib.auth.models import User  # type: ignore[import]

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} — {self.title}"


class BugReport(models.Model):
    PRIORITY = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    steps = models.TextField()
    expected = models.TextField()
    actual = models.TextField()
    browser = models.CharField(max_length=100, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY, default="medium")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
