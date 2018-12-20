from rest_framework import serializers
from lms.models.models import Student, Professor, Course, Group, Faculty, Task, Solution, Material


class RegistrationSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'group')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'email', 'group', 'study_base', 'study_form',
                  'phone', 'vk_link', 'fb_link', 'linkedin_link', 'insta_link')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'faculty', 'level', 'students')


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name', 'groups')


class ProfessorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('id', 'first_name', 'last_name')


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('id', 'first_name', 'last_name', 'phone', 'vk_link', 'fb_link', 'linkedin_link', 'insta_link', 'email')


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'professor', 'groups', 'headmen', 'tasks')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'text', 'course', 'start_time', 'finish_time')


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ('id', 'name', 'text', 'updated_at', 'course')


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ('id', 'text', 'task', 'created_at')
