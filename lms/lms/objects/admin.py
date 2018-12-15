from django.contrib import admin
from lms.objects.models import Student, Professor, Group, Course, Faculty, Task, Solution, Material


admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Group)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(Task)
admin.site.register(Solution)
admin.site.register(Material)