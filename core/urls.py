from django.urls import path
from . import views
urlpatterns = [
    #student dashboard
    path('dashboard/', views.student_dashboard, name='dashboard'),
    
    #Submit assignment
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    #Instructor dashboard
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    #view submission
    path('submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
    # create grading
    path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    
    
]


