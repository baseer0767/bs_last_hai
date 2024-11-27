from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
#from main.models import Profile
from authentication.models import Profile_main

class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField(default=timedelta(days=30))
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New attribute

class CourseContent(models.Model):
    course = models.ForeignKey(Course, related_name='contents', on_delete=models.CASCADE)
    Contenttitle = models.CharField(max_length=255)
    video = models.FileField(upload_to='course_videos/', max_length=255)
    content_type = models.CharField(max_length=100, choices=[('video', 'Video'), ('pdf', 'PDF'), ('text', 'Text')])
    order = models.IntegerField()
    additional_resources = models.FileField(upload_to='resources/', null=True, blank=True)
    is_last_video = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Contenttitle} ({self.content_type})"

class Quiz(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='quiz',null=True)
    title = models.CharField(max_length=255, editable=False)  # Make the title field non-editable

    def save(self, *args, **kwargs):
        # Set the title to match the course title
        if self.course:
            self.title = self.course.title
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Quiz for {self.course.title}" if self.course else "Quiz without Course"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[
        ('a', 'Option A'),
        ('b', 'Option B'),
        ('c', 'Option C'),
        ('d', 'Option D'),
    ])

    def check_answer(self, user_answer):
        return self.correct_answer == user_answer

    def _str_(self):
        return f"{self.quiz.title} - Question: {self.question_text[:50]}"  
    



class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')  # Student taking the quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')  # Quiz being attempted
    score = models.FloatField()  # Score of the quiz
    passed = models.BooleanField(default=False)  # Whether the student passed the quiz
    attempted_at = models.DateTimeField(auto_now_add=True)  # When the quiz was attempted
    correct_count = models.IntegerField(default=0)  # Add this field to store the correct answer count

    def __str__(self):
        return f"Quiz Attempt for {self.quiz.title} by {self.student.username}"


class VideoWatch(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    video_content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'video_content']

    def _str_(self):
        return f'{self.student.username} watched {self.video_content.Contenttitle}'   
    


class Certificate(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Certificate for {self.student.username} in {self.course.title}"
    
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class CourseFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user providing feedback
    quiz = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)  # The quiz being reviewed
    video_quality = models.IntegerField(null=True, blank=True, default=0)  # Rating for video quality (1-10)
    audio_quality = models.IntegerField(null=True, blank=True, default=0)  # Rating for audio quality (1-10)
    teaching_method = models.IntegerField(null=True, blank=True, default=0)  # Rating for teaching method (1-10)
    course_content = models.IntegerField(null=True, blank=True, default=0)  # Rating for course content (1-10)
    feedback = models.TextField(blank=True, null=True)  # Optional feedback
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp when feedback is submitted


    def __str__(self):
        return f"Feedback for Course: {self.quiz.quiz.title}"

    
