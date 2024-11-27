from django.contrib import admin
from .models import User, Student, Subscription

# Register your models here.

admin.site.register(Student)
admin.site.register(Subscription)