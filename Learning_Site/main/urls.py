from django.contrib import admin
from django.urls import path,include
#from .views import if_is_instructor,course_detail
from .import views
#from django.contrib.auth import views as auth_views
# from course_instructor.views import mark_video_watched
# from .views import your_view
from django.conf import settings
from django.conf.urls.static import static
from .views import main_page
from course_instructor.urls import mark_video_watched
from .import views

app_name = 'main'

urlpatterns = [
    # path("instructor",if_is_instructor,name='main'),
    path("",views.main_page,name='main_page'),
    path('mark-video-watched/', mark_video_watched, name='mark_video_watched'),
    path('profile/', views.User_Profile, name='user_profile'),
    # path('course/<int:course_id>/', course_detail, name='course_detail'),
    # path('registration/login/', auth_views.LoginView.as_view(), name='login'),
    # path('mark-video-watched/', mark_video_watched, name='mark_video_watched'),
    # path('your-view/', your_view, name='your_view'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
