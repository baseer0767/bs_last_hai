from django.db import models
from django.contrib.auth.models import User

class Profile_main(models.Model):
    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    msg = models.TextField(null=True, blank=True, default=None)
    city = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='learner')  # New field for role

    def __str__(self):
        return f"{self.user.username} ({self.role})"
