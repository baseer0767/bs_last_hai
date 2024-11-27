from django import forms
from .models import Student

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'email', 'date_of_birth', 'course_name', 'type', 'payment_method', 'payment_screenshot']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_screenshot': forms.FileInput(attrs={'class': 'form-control'}),
        }
