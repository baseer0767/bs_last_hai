# from django.db import models

# class Creator(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     bio = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     enrolled_courses = models.IntegerField(default=0)
#     joined_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
