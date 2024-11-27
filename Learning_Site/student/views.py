from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Subscription
from .forms import SubscriptionForm
from course_instructor.models import Course
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def unpaid_courses(request):
    return render(request, 'content.html')

def paid_courses(request):
    return render(request, 'content.html')

@login_required
def subscribe(request, course_name, course_type):
    print(f"Course Name: {course_name}, Course Type: {course_type}")  # Debugging line

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid, saving...")  # Debugging line
            student_data = form.save(commit=False)  # Get the student instance
            
            # Assign the logged-in user if available
            if request.user.is_authenticated:
                 student_data.user = request.user
            
            student_data.course_name = course_name  # Set course_name automatically
            student_data.type = course_type  # Set course_type automatically
            
            # Handle paid course validation
            if course_type == 'paid':
                if not student_data.payment_method:
                    form.add_error('payment_method', 'Payment method is required for paid courses.')
                payment_screenshot = request.FILES.get('payment_screenshot')
                if not payment_screenshot:
                    form.add_error('payment_screenshot', 'Payment screenshot is required for paid courses.')
                else:
                    student_data.payment_screenshot = payment_screenshot  # Assign the file to the model field
            
            # Save the student data only if there are no errors
            if not form.errors:
                student_data.save()
                print("Student data saved successfully.")

                # Save subscription details
                subscription = Subscription(
                    user=student_data.user,
                    student=student_data,
                    course_title=course_name,
                    course_type=course_type,

                )
                subscription.save()
                print("Subscription saved successfully.")
                
                return render(request, 'subscribe.html', {'subscription_success': True, 'course_name': course_name})
            else:
                print(f"Form errors: {form.errors}")
        else:
            print(f"Form is invalid: {form.errors}")
    else:
        # Pre-fill form with course name and type
        form = SubscriptionForm(initial={'course_name': course_name, 'type': course_type})

    return render(request, 'subscribe.html', {'form': form, 'course_name': course_name, 'course_type': course_type})

def home(request):
    return render(request,'content.html')
