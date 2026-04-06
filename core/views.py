from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Enrollment, Assignment, Submission, Course


#Student Dashboard

@login_required
def student_dashboard(request):
    user = request.user

    if user.role == 'instructor':
        return redirect('instructor_dashboard') # we' wil build next
    
    # Get enrollments for logged-in student
    enrollments = Enrollment.objects.filter(student=user)
    courses = [en.course for en in enrollments]
    assignments = Assignment.objects.filter(course__in=courses)
    submissions = Submission.objects.filter(student=user)

    # 🔥 ANALYTICS
    total_courses = len(courses)
    total_assignments = assignments.count()
    submitted = submissions.count()
    pending = total_assignments - submitted

    return render(request, 'core/dashboard.html', {
        'enrollments': enrollments,
        'assignments': assignments,
        'submissions': submissions,

        # analytics
        'total_courses': total_courses,
        'total_assignments': total_assignments,
        'submitted': submitted,
        'pending': pending,
    })


     # Extract courses
    courses = [en.course for en in enrollments]

    # Get assignments for those courses
    assignments = Assignment.objects.filter(course__in=courses)
    print("Courses:", courses)
    print("Assignments:", assignments)
    return render(request, 'core/dashboard.html', {
        'enrollments': enrollments,
        'assignments':assignments,
     
    
    })
              
    

#submit Assignment

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        file = request.FILES.get('file')

        #save submission
        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=file
        )
        return redirect('dashboard')

    return render(request, 'core/submit.html', {
        'assignment': assignment
    })


#Instructor dashboard
@login_required
def instructor_dashboard(request):
    user = request.user

    # Get courses taught by instructor
    courses = Course.objects.filter(instructor=user)
    
    # Get assignments for those courses
    assignments = Assignment.objects.filter(course__in=courses)

    return render(request, 'core/instructor_dashboard.html', {
        'courses': courses,
        'assignments': assignments
    })

# Viewing Submissions
@login_required
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    submissions = Submission.objects.filter(assignment=assignment)

    return render(request, 'core/submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })
 
# Create Grading View

@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.method == 'POST':
        submission.grade = request.POST.get('grade')
        submission.feedback = request.POST.get('feedback')
        submission.save()

        return redirect('view_submissions', assignment_id=submission.assignment.id)

    return render(request, 'core/grade.html', {
        'submission': submission
    })
