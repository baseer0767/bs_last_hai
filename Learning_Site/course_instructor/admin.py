from django.contrib import admin

# Register your models here.
from .models import Course,CourseContent
from .models import Quiz, Question,VideoWatch,QuizAttempt,CourseFeedback


class CourseAdmin(admin.ModelAdmin):
    pass
admin.site.register(Course, CourseAdmin)

class CourseContentAdmin(admin.ModelAdmin):
    pass
admin.site.register(CourseContent, CourseContentAdmin)

class QuizAdmin(admin.ModelAdmin):
    pass

admin.site.register(Quiz,QuizAdmin)

class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Question,QuestionAdmin)

class VideoWatchAdmin(admin.ModelAdmin):
    pass

admin.site.register(VideoWatch,VideoWatchAdmin)

class QuizAttemptAdmin(admin.ModelAdmin):
     pass

admin.site.register(QuizAttempt,QuizAttemptAdmin)

from .models import Certificate

class CertificateAdmin(admin.ModelAdmin):
    pass

admin.site.register(Certificate,CertificateAdmin)

admin.site.register(CourseFeedback)
