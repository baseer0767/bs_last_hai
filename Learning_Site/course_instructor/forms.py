from django import forms
from course_instructor.models import Course, CourseContent
from .models import Quiz, Question

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description','course_type', 'duration', 'price']  # Fields to be edited by the instructor


class CourseContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        fields = ['Contenttitle', 'video', 'content_type', 'order', 'additional_resources','is_last_video']


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']

from django import forms
from .models import CourseFeedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['video_quality', 'audio_quality', 'teaching_method', 'course_content', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your feedback here...'}),
        }
