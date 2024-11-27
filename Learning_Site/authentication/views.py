from django.shortcuts import render, redirect
from .form import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Profile_main
from main.views import main_page
from main.urls import main_page


def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')  # Get the selected role
        request.session['user_role'] = role  # Save role in session

        if role == 'admin':  # Check if the selected role is "Admin"
            return redirect('authentication:login')  # Redirect to the login page
        else:
            return redirect('authentication:register')  # Redirect to the registration page
    
    return render(request, 'select_role.html')


def register(request):
    role = request.session.get('user_role')  # Retrieve the role from session
    if not role:
        return redirect('authentication:select_role')  # If role is not set, ask the user to select it
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Create or update profile with the role from session
            profile, created = Profile_main.objects.get_or_create(user=user)
            profile.city = form.cleaned_data['city']
            profile.role = role  # Set the role from session
            profile.save()

            return redirect('authentication:login')

    else:
        form = UserRegistrationForm()  # Initialize an empty form for GET requests

    return render(request, 'register.html', {'form': form})


from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Get user role from session or user object
            role = request.session.get('user_role')  # Ensure 'user_role' is set in session elsewhere
            if role == 'admin':  # Check if the user's role is 'admin'
                return redirect('authentication:list_all_user')  # Redirect to the list all users page
            else:
                return redirect('main:main_page')  # Redirect to the main page for other roles
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Profile_main

# Custom function to check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

# Use the decorator to ensure only superusers can access this view
@user_passes_test(is_superuser)
def list_all_users(request):
    # Since this view is only for admins, we don't need further authentication checks here
    if request.user.is_authenticated:  # Ensure the user is logged in (though it's already guaranteed by the decorator)
        if request.user.is_superuser:  # Ensure the user is a superuser (this should always be True here)
            # Fetch all users from Profile_main (this will not check roles, admins can see all users)
            all_users = Profile_main.objects.all()

            context = {
                'all_users': all_users,
            }

            return render(request, 'list_all_users.html', context)
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect('authentication:register')
    
from django.shortcuts import render, get_object_or_404
from course_instructor.models import Course
from student.models import Subscription

def user_details(request, username):
    # Fetch the user's profile based on their username
    user_profile = get_object_or_404(Profile_main, user__username=username)

    # Fetch courses based on the user's role
    if user_profile.role == 'learner':
        # Fetch subscriptions for the logged-in learner
        subscriptions = Subscription.objects.filter(user=user_profile.user)
        courses = Course.objects.filter(title__in=[sub.course_title for sub in subscriptions])
    elif user_profile.role == 'instructor':
        # Fetch courses created by the instructor
        courses = Course.objects.filter(instructor=user_profile.user)
    else:
        courses = None  # For other roles, no courses are displayed

    context = {
        'user_profile': user_profile,
        'courses': courses,  # Add the list of courses to the context
    }

    return render(request, 'user_details.html', context)




from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Profile_main
from django.contrib.auth.models import User

# View to delete a user profile based on username
@user_passes_test(is_superuser)
def delete_user(request, username):
    if request.method == "POST":
        # Get the user by username
        user_profile = get_object_or_404(Profile_main, user__username=username)
        
        # Delete the associated profile and user
        user_profile.user.delete()
        
        # Display a success message
        messages.success(request, f"User {username} deleted successfully.")
        
        # Redirect to the list of all users
        return redirect('authentication:list_all_user')

    return redirect('authentication:list_all_user')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from course_instructor.models import Course
from django.contrib.auth.decorators import user_passes_test

# Custom function to check if the user is a superuser
def is_superuser(user):
    return user.is_superuser

# Delete the course view
@user_passes_test(is_superuser)
def delete_course(request, course_id):
    # Get the course by ID
    course = get_object_or_404(Course, id=course_id)
    
    # Delete the course (admins can delete any course)
    course.delete()
    messages.success(request, f"Course '{course.title}' deleted successfully.")
    
    # Redirect back to the user details page of the instructor who created the course
    return redirect('authentication:user_details', username=course.instructor.username)





    




