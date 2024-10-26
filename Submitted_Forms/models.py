from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SubmittedForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    form_title = models.CharField(max_length=200)
    file = models.FileField(upload_to='submitted_forms/')
    created_at = models.DateTimeField(default=timezone.now)
    is_reviewed = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    admin_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s submission for {self.form_title}"
