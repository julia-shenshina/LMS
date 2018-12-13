from rest_framework import viewsets
from lms.objects.serializers import StudentSerializer, GroupSerializer, FacultySerializer, ProfessorSerializer, CourseSerializer
from lms.objects.models import Student, Professor, Course, Group, Faculty


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('last_name')
    serializer_class = StudentSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all().order_by('name')
    serializer_class = FacultySerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('last_name')
    serializer_class = ProfessorSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('name')
    serializer_class = CourseSerializer

