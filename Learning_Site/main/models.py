# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.Model):
#     # Linking Profile to Django's built-in User model for authentication
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     # General profile information
#     bio = models.TextField(blank=True, null=True)  # Short biography or description of the user
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Optional profile picture

#     # Role indicators for the user
#     is_student = models.BooleanField(default=False)  # Indicates if the user is a student
#     is_instructor = models.BooleanField(default=False)  # Indicates if the user is an instructor

#     # Additional fields specific to instructors
#     instructor_bio = models.TextField(blank=True, null=True)  # Detailed bio for instructors
#     expertise = models.CharField(max_length=255, blank=True, null=True)  # Area of expertise (e.g., subject or field)

#     # Timestamps for profile creation and updates
#     created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the profile is created
#     updated_at = models.DateTimeField(auto_now=True)  # Automatically updated when the profile is modified

#     def __str__(self):
#         # Display the username associated with the profile
#         return self.user.username

#     # Helper methods to identify the role of the user
#     def is_student_only(self):
#         # Returns True if the user is only a student
#         return self.is_student and not self.is_instructor

#     def is_instructor_only(self):
#         # Returns True if the user is only an instructor
#         return self.is_instructor and not self.is_student

#     def is_both(self):
#         # Returns True if the user is both a student and an instructor
#         return self.is_student and self.is_instructor
