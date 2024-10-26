from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import URLValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Student', 'Student'),
        ('Mentor', 'Mentor')
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Student')
    is_verified = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("can_view_profile", "Can view profile"),
            ("can_edit_profile", "Can edit profile"),
        ]

    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(validators=[URLValidator()], blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(User, related_name='skills')

    def __str__(self):
        return self.name

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.role_name}"

class Verification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Verification"

class MentorRequest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_requests')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentees')
    request_date = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Request from {self.student.username} to {self.mentor.username}"
