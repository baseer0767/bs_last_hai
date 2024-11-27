from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import list_all_users, user_details

app_name = 'authentication'
from .views import list_all_users
urlpatterns = [
    path('learner-register',views.register, name='register'),
    path('select-role/', views.select_role, name='select_role'),  # Role selection page
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('all-users/', list_all_users, name='list_all_user'),
    path('user/<str:username>/', user_details, name='user_details'),
    path('delete-user/<str:username>/', views.delete_user, name='delete_user'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),


]

