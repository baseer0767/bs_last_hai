from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from course_instructor.models import Course, CourseContent

# def if_is_instructor(request):
#     return render(request, "if_is_instructor.html")

from django.contrib.auth.decorators import login_required

@login_required
def main_page(request):
    query = request.GET.get('q', '').strip()  # Get the search query from the URL, strip whitespace
    if request.user.profile_main.role == 'instructor':
        # Fetch only courses created by the logged-in instructor
        courses = Course.objects.filter(instructor=request.user)
    else:
        courses = Course.objects.all()
    
    # Filter courses only if there is a query
    if query:
        courses = courses.filter(title__icontains=query)

    return render(request, 'main_page.html', {'courses': courses, 'query': query})

from student.models import Subscription

def User_Profile(request):
    if request.user.profile_main.role == 'learner':
        # Fetch subscriptions for the logged-in learner
        subscriptions = Subscription.objects.filter(user=request.user)
        # Fetch courses corresponding to the subscriptions
        courses = Course.objects.filter(title__in=[sub.course_title for sub in subscriptions])
    else:
        # For other roles, show all courses or modify as per requirements
        courses = Course.objects.all()

    return render(request, 'profile.html', {'courses': courses})

# def main_page(request):
#     # Fetch all courses
#     courses = Course.objects.all()  # You can filter this as per your requirements
#     return render(request, 'main_page.html', {'courses': courses})

# def course_detail(request, course_id):
#     # Get the course and its contents
#     course = get_object_or_404(Course, id=course_id)
#     course_contents = CourseContent.objects.filter(course=course)

#     context = {
#         'course': course,
#         'course_contents': course_contents,
#         'student_id': request.user.id,  # Pass user.id as student_id
#     }
#     return render(request, 'course_detail.html', context)

# def your_view(request):
#     student_id = request.user.id  # Assuming the logged-in user is the student
#     context = {'student_id': student_id}
#     return render(request, 'your_view.html', context)
