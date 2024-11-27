from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('unpaid-courses/', views.unpaid_courses, name='unpaid_courses'),
    path('paid-courses/', views.paid_courses, name='paid_courses'),
    path('subscribe/<str:course_name>/<str:course_type>/', views.subscribe, name='subscribe'),
    path('home', views.home, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
