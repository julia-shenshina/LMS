from uuid import uuid4

from django.utils import timezone
from rest_framework import viewsets, views, generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers

from lms.api import serializers
from lms.api import permissions, utils
from lms.models.models import Student, Professor, Group, Faculty, Material, Task, Solution, Course


class StudentViewSet(viewsets.mixins.RetrieveModelMixin,
                     viewsets.mixins.UpdateModelMixin,
                     viewsets.mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
    For student return a list of groupmates, for professor return a list of students of professor'a courses

    retrieve:
    Return student with id

    update:
    Change student's account info
    """
    queryset = Student.objects.all().order_by('last_name')
    serializer_class = serializers.StudentSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.StudentListSerializer

        return serializers.StudentSerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, Student):
            group = Group.objects.filter(id=user.group.id).first()
            queryset = Student.objects.filter(group=group).all().order_by('last_name')
        else:

            queryset = Student.objects.filter(group__courses__professor=user)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if not permissions.can_view_study_base(self.request.user, instance):
            data.pop('study_base')
        return Response(data)

    def update(self, request, *args, **kwargs):
        if not permissions.can_edit_student_profile(self.request.user, self.get_object()):
            raise PermissionDenied('You have no permissions to update account.')

        return super().update(request, *args, **kwargs)


class GroupViewSet(viewsets.mixins.RetrieveModelMixin,
                   viewsets.mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    list:
    Return a list of groups

    retrieve:
    Return group with id
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = serializers.GroupSerializer


class FacultyViewSet(viewsets.mixins.RetrieveModelMixin,
                     viewsets.mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
    Return a list of faculties

    retrieve:
    Return faculty with id
    """
    queryset = Faculty.objects.all().order_by('name')
    serializer_class = serializers.FacultySerializer

    def get_absolute_url(self):
        return 'faculties/%i' % self.id


class ProfessorViewSet(viewsets.mixins.RetrieveModelMixin,
                       viewsets.mixins.UpdateModelMixin,
                       viewsets.mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
    Return a list of professors

    retrieve:
    Return professor with id

    update:
    Change professor's account info
    """
    queryset = Professor.objects.all().order_by('last_name')
    serializer_class = serializers.ProfessorSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProfessorListSerializer

        return serializers.ProfessorSerializer

    def update(self, request, *args, **kwargs):
        if not permissions.can_edit_professor_profile(self.request.user, self.get_object()):
            raise PermissionDenied()

        return super().update(request, *args, **kwargs)


class CourseViewSet(viewsets.mixins.RetrieveModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    retrieve:
    Return course with id

    list:
    Return list of user's courses

    update:
    Add headmen to the course
    """
    serializer_class = serializers.CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, Student):
            queryset = user.group.courses.all()
        else:
            queryset = user.courses.all()
        return queryset.order_by('name')

    def update(self, request, *args, **kwargs):
        user = request.user
        course = self.get_object()
        if not permissions.can_add_headman(user, course):
            raise PermissionDenied('You have no permissions to add headmen to this course.')

        student_ids = request.data.get('headmen')
        students = Student.objects.filter(id__in=student_ids).all()
        if not permissions.can_be_headman(students, course):
            raise ValidationError('This student has not this course')

        return super().update(request, *args, **kwargs)


class MaterialViewSet(viewsets.ModelViewSet):
    """
    list:
    Returns user's courses list materials

    retrieve:
    Return material with id

    create:
    Create course material

    update:
    Update course material

    delete:
    Delete course material
    """
    serializer_class = serializers.MaterialSerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, Student):
            courses = user.group.courses.all()
        else:
            courses = user.courses.all()

        queryset = Material.objects.filter(course__in=courses).all().order_by('updated_at')
        return queryset

    def perform_create(self, serializer):
        request = serializer.context['request']

        course_id = request.data.get('course')
        course = Course.objects.filter(id=course_id).first()

        if not permissions.can_create_course_materials(request.user, course):
            raise PermissionDenied('You have no permissions to create materials.')

        if not course:
            raise ValidationError('No course with this id.')

        return serializer.save(course=course)

    def update(self, request, *args, **kwargs):
        if not permissions.can_edit_course_materials(self.request.user, self.get_object().course):
            raise PermissionDenied('You have no permissions to modify materials.')

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not permissions.can_delete_course_materials(self.request.user, self.get_object().course):
            raise PermissionDenied('You have no permissions to delete materials.')

        return super().destroy(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of tasks of user's courses

    retrieve:
    Return task with id

    update:
    Update task with id

    create:
    Create task
    """
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        """Get tasks for user's courses"""
        user = self.request.user
        if isinstance(user, Student):
            courses = user.group.courses.all()
            today = timezone.now().date()
            queryset = Task.objects.filter(course__in=courses, start_time__lte=today, finish_time__gte=today).all()
        else:
            courses = user.courses.all()
            queryset = Task.objects.filter(course__in=courses).all()

        return queryset.order_by('start_time')

    def update(self, request, *args, **kwargs):
        if not permissions.can_edit_course_tasks(self.request.user, self.get_object().course):
            raise PermissionDenied('You have no permissions to modify the task.')

        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        request = serializer.context['request']

        course_id = request.data.get('course')
        course = Course.objects.filter(id=course_id).first()

        if not permissions.can_create_course_tasks(request.user, course):
            raise PermissionDenied('You have no permissions to create tasks.')

        return serializer.save()

    def destroy(self, request, *args, **kwargs):
        if not permissions.can_delete_course_materials(self.request.user, self.get_object().course):
            raise PermissionDenied('You have no permissions to delete tasks.')

        return super().destroy(request, *args, **kwargs)


class SolutionViewSet(viewsets.mixins.CreateModelMixin,
                      viewsets.mixins.RetrieveModelMixin,
                      viewsets.mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    list:
    Return a list of user's solutions

    retrieve:
    Return solution with id

    create:
    Create solution
    """
    serializer_class = serializers.SolutionSerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, Student):
            queryset = user.solutions.all()
        else:
            courses = user.courses.all()
            queryset = Solution.objects.filter(course__in=courses).order_by('student__group').all()

        return queryset.order_by('created_at')

    def perform_create(self, serializer):
        request = serializer.context['request']
        if not permissions.can_submit_solution(request.user):
            raise PermissionDenied('Only student cant submit solutions.')

        task_id = request.data.get('task')
        today = timezone.now().date()
        task = Task.objects.filter(id=task_id, start_time__lte=today, finish_time__gte=today).first()
        if not task:
            raise ValidationError('The task has not begun yet or already has finished.')

        return serializer.save(student=request.user, task=task)


class RegistrationView(generics.GenericAPIView):
    """
    post:
    Registration of pre-registered user
    """
    authentication_classes = ()
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = serializers.RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError("Token, email and password should be provided")

        person = utils.get_student_or_professor(token=serializer.data['token'])
        if person is None:
            raise ValidationError("No token")

        person.email = serializer.data['email']
        person.password = serializer.data['password']
        person.token = None
        person.save(update_fields=['email', 'password', 'token'])
        return views.Response('ok')


class LoginView(views.APIView):
    """
    post:
    Login for reistered user, return secret_key
    """
    authentication_classes = ()

    def post(self, request):
        """ Login user and return secret key for next requests"""
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if not all((email, password)):
            raise ValidationError('Email and password should be provided.')

        person = utils.get_student_or_professor(email=email, password=password)
        if person is None:
            raise ValidationError("No token.")

        person.secret_key = uuid4().hex
        person.save(update_fields=['secret_key'])
        return views.Response({'secret_key': person.secret_key})


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    class SwaggerSchemaView(APIView):
        """Returns a list of API documentation"""
        authentication_classes = ()

        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            generator = SchemaGenerator(
                title=title,
                url=url,
                patterns=patterns,
                urlconf=urlconf
            )
            schema = generator.get_schema(request=request)

            if not schema:
                raise ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()
