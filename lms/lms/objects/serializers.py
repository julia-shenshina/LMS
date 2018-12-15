from rest_framework import serializers
from lms.objects.models import Student, Professor, Course, Group, Faculty, Task, Solution, Material


class StudentListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'group')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email', 'group', 'study_base', 'study_form',
                  'phone', 'vk_link', 'fb_link', 'linkedin_link', 'insta_link')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'faculty', 'level', 'students')


class FacultySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name', 'groups')


class ProfessorListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ('id', 'first_name', 'last_name')


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ('id', 'first_name', 'last_name', 'phone', 'vk_link', 'fb_link', 'linkedin_link', 'insta_link', 'email')


class CourseListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'professor', 'groups', 'headmen')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'text', 'course', 'start_time', 'finish_time')


class MaterialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'text', 'updated_at', 'course')


class SolutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Solution
        fields = ('id', 'text', 'task')
