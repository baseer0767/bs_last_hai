from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    COURSE_TYPE_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]

    PAYMENT_METHOD_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('paypal', 'PayPal'),
    ('bank_transfer', 'Bank Transfer'),
]
    
    # Make user field optional by using null=True and blank=True
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    subscripted_at = models.DateTimeField(auto_now_add=True)
    course_name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', null=True, blank=True)  


    def __str__(self):
        return self.full_name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_title = models.CharField(max_length=100)
    course_type = models.CharField(max_length=10, choices=Student.COURSE_TYPE_CHOICES)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course_title}"
