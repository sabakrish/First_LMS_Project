
from django.contrib import admin
from .models import User, Course, Enrollment, Assignment, Submission

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(Submission)