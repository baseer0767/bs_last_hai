from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.forms import formset_factory
from django.urls import reverse
from django.utils.timezone import now
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from django.db.models import Prefetch
import json
from django.utils import timezone
from django.db.models import Max
from .models import (
    Course, CourseContent, VideoWatch, Quiz, Question, QuizAttempt, Certificate
)
from .forms import CourseForm, CourseContentForm, QuizForm, QuestionForm
from authentication.models import Profile_main

def create_course(request):
    if request.user.profile_main.role != 'instructor':
        raise PermissionDenied("You must be an instructor to create a course.")
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user  # Use the User model directly here
            course.save()
            return redirect(reverse('add_update_content', args=[course.id]))
    else:
        form = CourseForm()

    return render(request, 'registration/create_course.html', {'form': form})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_contents = CourseContent.objects.filter(course=course).order_by('order')

    return render(
        request,
        'course_detail.html',
        {
            'course': course,
            'course_contents': course_contents,
            'student_id': request.user.id,  # Add this for potential logged-in student tracking
        }
    )

# Filter courses by type (paid/unpaid/all)
def filter_courses(request):
    course_type = request.GET.get('type', 'all')
    content_prefetch = Prefetch(
        'contents',
        queryset=CourseContent.objects.all().order_by('order')
    )
    if course_type == 'paid':
        courses = Course.objects.filter(course_type='paid').prefetch_related(content_prefetch)
    elif course_type == 'unpaid':
        courses = Course.objects.filter(course_type='unpaid').prefetch_related(content_prefetch)
    else:
        courses = Course.objects.all().prefetch_related(content_prefetch)

    return render(request, 'course_list.html', {'courses': courses, 'selected_type': course_type})

# def add_update_content(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     if request.method == "POST":
#         form = CourseContentForm(request.POST, request.FILES)
#         if form.is_valid():
#             course_content = form.save(commit=False)
#             course_content.course = course
#             course_content.save()
#             messages.success(request, 'Content added successfully!')
#             #return redirect('success_page')
#     else:
#         form = CourseContentForm()

#     return render(request, 'registration/add_update_content.html', {'form': form, 'course': course})

# from django.urls import reverse

# def add_update_content(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     if request.method == "POST":
#         form = CourseContentForm(request.POST, request.FILES)
#         if form.is_valid():
#             course_content = form.save(commit=False)
#             course_content.course = course
#             course_content.save()
#             messages.success(request, 'Content added successfully!')

#             # Redirect to the create_quiz view
#             return redirect(reverse('create_quiz', args=[course.id]))
#     else:
#         form = CourseContentForm()

#     return render(request, 'registration/add_update_content.html', {'form': form, 'course': course})

from django.forms import modelformset_factory

def add_update_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Create a formset for CourseContent
    CourseContentFormSet = modelformset_factory(CourseContent, form=CourseContentForm, extra=5)

    if request.method == "POST":
        formset = CourseContentFormSet(request.POST, request.FILES)
        
        if formset.is_valid():
            for form in formset:
                course_content = form.save(commit=False)
                course_content.course = course

                # Assign order for each content
                max_order = CourseContent.objects.filter(course=course).aggregate(Max('order'))['order__max'] or 0
                course_content.order = max_order + 1

                # Optionally mark the last video (if 'is_last_video' is set)
                if course_content.content_type == 'video' and form.cleaned_data.get('is_last_video', False):
                    course_content.is_last_video = True

                course_content.save()

            messages.success(request, 'Content added successfully!')
            return redirect(reverse('create_quiz', args=[course.id]))

    else:
        formset = CourseContentFormSet(queryset=CourseContent.objects.none())

    return render(request, 'registration/add_update_content.html', {'formset': formset, 'course': course})


# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'
#     redirect_authenticated_user = True

#     def form_valid(self, form):
#         user = form.get_user()
#         if user.profile.is_instructor:
#             login(self.request, user)
#             return redirect('create_course')
#         else:
#             raise PermissionDenied("You must be an instructor to access this page.")


# from django.views.decorators.csrf import csrf_protect
# @csrf_protect
# def mark_video_watched(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             video_id = data.get('video_id')
#             student_id = data.get('student_id')

#             # Find the video content by ID
#             video_content = CourseContent.objects.get(id=video_id)
#             student = User.objects.get(id=student_id)

#             # Update the 'watched' status in the VideoWatch table
#             video_watch, created = VideoWatch.objects.get_or_create(
#                 student=student,
#                 video_content=video_content
#             )
#             video_watch.watched = True
#             video_watch.watched_at = timezone.now()  # Set the time when it was watched
#             video_watch.save()

#             # Check if the video is marked as the last video
#             if video_content.is_last_video is True:
#                 # Check for an associated quiz
#                 # quiz = Quiz.objects.filter(Course.title).first()
#                 quiz = Quiz.objects.filter(course=video_content.course).first()
#                 if quiz:
#                     quiz_url = reverse('quiz_view', args=[quiz.id])  # changed video id to quiz id
#                     # return redirect('quiz_view', quiz_id=quiz.id)
#                     return JsonResponse({'status': 'success', 'quiz_url': quiz_url}, status=200)
#                 else:
#                     return JsonResponse({'status': 'error', 'message': 'No quiz available for this video.'}, status=404)

#             # If not the last video, just mark as watched and return success
#             return JsonResponse({'status': 'success', 'message': 'Video marked as watched.'}, status=200)

#         except CourseContent.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Video not found'}, status=404)

#         except User.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

from django.views.decorators.csrf import csrf_protect

@csrf_protect

def mark_video_watched(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            video_id = data.get('video_id')
            student_id = data.get('student_id')

            # Find the video content by ID
            video_content = CourseContent.objects.get(id=video_id)
            student = User.objects.get(id=student_id)

            # Update the 'watched' status in the VideoWatch table
            video_watch, created = VideoWatch.objects.get_or_create(
                student=student,
                video_content=video_content
            )
            video_watch.watched = True
            video_watch.watched_at = timezone.now()  # Set the time when it was watched
            video_watch.save()

            # Check if the video is marked as the last video
            if video_content.is_last_video is True:
                # Check for an associated quiz
                # quiz = Quiz.objects.filter(Course.title).first()
                quiz = Quiz.objects.filter(course=video_content.course).first()
                if quiz:
                    quiz_url = reverse('quiz_view', args=[quiz.id])  # changed video id to quiz id
                    # return redirect('quiz_view', quiz_id=quiz.id)
                    return JsonResponse({'status': 'success', 'quiz_url': quiz_url}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': 'No quiz available for this video.'}, status=404)

            # If not the last video, just mark as watched and return success
            return JsonResponse({'status': 'success', 'message': 'Video marked as watched.'}, status=200)

        except CourseContent.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Video not found'}, status=404)

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)


@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == "POST":
        answers = request.POST.dict()
        correct_count = sum(
            1 for question in quiz.questions.all() if question.check_answer(answers.get(f'question_{question.id}'))
        )

        score = (correct_count / 10) * 100
        passed = score >= 70

        QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
            score=score,
            passed=passed,
            correct_count=correct_count
        )

        if passed:
            Certificate.objects.get_or_create(
                student=request.user,
                course=quiz.course
            )

        return render(request, 'quiz_result.html', {
            'score': score,
            'quiz': quiz,
            'passed': passed,
            'correct_count': correct_count,
            'certificate_created': passed
        })

    return render(request, 'registration/quiz.html', {'quiz': quiz, 'questions': quiz.questions.all()})


def create_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if hasattr(course, 'quiz'):
        return JsonResponse({'message': 'Quiz already exists for this course.'}, status=400)

    QuestionFormSet = formset_factory(QuestionForm, extra=10)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)

        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.course = course
            quiz.save()

            for form in question_formset:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()

            return redirect('course_detail', course.id)

    quiz_form = QuizForm(initial={'title': f"Quiz for {course}"})
    question_formset = QuestionFormSet()

    return render(request, 'registration/create_quiz.html', {'quiz_form': quiz_form, 'question_formset': question_formset})


def edit_course_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not (request.user.profile_main.role == 'instructor'):
        return HttpResponseForbidden("You are not allowed to edit this course.")

    contents = CourseContent.objects.filter(course=course).order_by('order')

    if request.method == 'POST':
        content_id = request.POST.get('content_id')
        action = request.POST.get('action')

        if action == 'delete' and content_id:
            content = get_object_or_404(CourseContent, id=content_id, course=course)
            content.delete()
            return redirect('edit_course_content', course_id=course.id)

        if action == 'update' and content_id:
            content = get_object_or_404(CourseContent, id=content_id, course=course)
            content.Contenttitle = request.POST.get('title', content.Contenttitle)
            content.order = request.POST.get('order', content.order)

            if 'video' in request.FILES:
                content.video = request.FILES['video']

            content.save()
            return redirect('edit_course_content', course_id=course.id)

    return render(request, 'edit_course_content.html', {'course': course, 'contents': contents})

def generate_certificate(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{course.id}.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(colors.green)
    p.drawString(200, 750, "Certificate of Completion")

    p.setFont("Helvetica", 18)
    p.setFillColor(colors.black)
    p.drawString(100, 700, f"This is to certify that")

    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 670, f"{request.user.username} has successfully completed")

    p.setFont("Helvetica", 18)
    p.setFillColor(colors.black)
    p.drawString(100, 640, f"Course: {course.title}")

    p.setFont("Helvetica-Oblique", 16)
    p.setFillColor(colors.black)
    p.drawString(100, 600, "Date of Completion: " + str(course.created_at))

    p.setFont("Helvetica", 14)
    p.drawString(100, 570, "Congratulations!")

    p.showPage()
    p.save()

    return response

def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            if quiz.questions.count() == 10:
                return redirect('quiz_success')  # Redirect after all 10 questions are added
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()

    return render(request, 'registration/add_questions.html', {'question_form': question_form, 'quiz': quiz})

# @login_required
# def edit_course_content(request, course_id):
#     course = get_object_or_404(Course, id=course_id)

#     # Check if the user is the instructor of the course
#     if not (request.user.profile.is_instructor and course.instructor == request.user.profile):
#         return HttpResponseForbidden("You are not allowed to edit this course.")

#     # Fetch all contents of the course
#     contents = CourseContent.objects.filter(course=course).order_by('order')

#     if request.method == 'POST':
#         content_id = request.POST.get('content_id')
#         action = request.POST.get('action')

#         if action == 'delete' and content_id:
#             # Handle content deletion
#             content = get_object_or_404(CourseContent, id=content_id, course=course)
#             content.delete()
#             return redirect('edit_course_content', course_id=course.id)

#         if action == 'update' and content_id:
#             # Handle content updates
#             content = get_object_or_404(CourseContent, id=content_id, course=course)
#             content.Contenttitle = request.POST.get('title', content.Contenttitle)
#             content.order = request.POST.get('order', content.order)

#             # Handle video file update
#             if 'video' in request.FILES:
#                 content.video = request.FILES['video']

#             content.save()
#             return redirect('edit_course_content', course_id=course.id)

#     return render(request, 'edit_course_content.html', {'course': course, 'contents': contents})




def delete_course_content(request, content_id):
    content = get_object_or_404(CourseContent, id=content_id)
    course = content.course
    
    # Check if the user is the instructor of the course
    if not (request.user.profile.is_instructor and course.instructor == request.user.profile):
        return HttpResponseForbidden("You are not allowed to delete this content.")
    
    if request.method == 'POST':
        content.delete()
        return redirect('course_detail', course_id=course.id)

    return render(request, 'delete_course_content_confirm.html', {'content': content, 'course': course})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if the user is the instructor
    # if not (request.user.profile_main.role == 'instructor' and course.instructor == request.user.profile_main):
    if not (request.user.profile_main.role == 'instructor'):
        return HttpResponseForbidden("You are not allowed to edit this course.")
    
    if request.method == 'POST':
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.duration = request.POST.get('duration', course.duration)
        course.save()
        return redirect('course_detail', course_id=course.id)

    return render(request, 'edit_course.html', {'course': course})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if the user is the instructor
    if not (request.user.profile.is_instructor and course.instructor == request.user.profile):
        return HttpResponseForbidden("You are not allowed to delete this course.")
    
    if request.method == 'POST':
        course.delete()
        return redirect('all_courses')  # Redirect to a list of all courses

    return render(request, 'delete_course_confirm.html', {'course': course})


from django.shortcuts import render, redirect, get_object_or_404
from .models import QuizAttempt
from .forms import FeedbackForm

def feedback_view(request, quiz_id):
    quiz = get_object_or_404(QuizAttempt, id=quiz_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.quiz = quiz
            feedback.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form, 'quiz': quiz})


def thank_you(request):
    return render(request, 'thank_you.html')
