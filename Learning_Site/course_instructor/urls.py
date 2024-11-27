
from django.contrib import admin
from django.urls import path,include
from .views import create_course,add_update_content,create_quiz,add_questions,quiz_view,mark_video_watched,generate_certificate,edit_course_content,delete_course_content,delete_course,edit_course,filter_courses
from django.http import HttpResponse
from .views import course_detail
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("create_course",create_course,name='create_course'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path("add_update_content/<int:course_id>/",add_update_content,name='add_update_content'),
    path('add-questions/<int:quiz_id>/',add_questions, name='add_questions'),
    path('quiz/<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('create-quiz/<int:course_id>/',create_quiz, name='create_quiz'),
    path("courses/", filter_courses, name="filter_courses"),    
    path('generate_certificate/<int:course_id>/', generate_certificate, name='generate_certificate'),
    path('edit-course/<int:course_id>/', edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', delete_course, name='delete_course'),
    path('edit-course-content/<int:course_id>/', edit_course_content, name='edit_course_content'),
    path('delete-content/<int:content_id>/',delete_course_content, name='delete_course_content'),
    path('quiz/<int:quiz_id>/feedback/', views.feedback_view, name='feedback'),
    path('thank-you/', views.thank_you, name='thank_you'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)