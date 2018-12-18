from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from lms.models.models import Course, Faculty, Group, Professor, Student, Solution, Task


class TestSolution(APITestCase):
    def test_create_solution_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.groups.set([group])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name="Задача_1", text="Текст задачи_1", start_time=today, finish_time=today + delta, course=course
        )
        course.refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.post(
            reverse('solution-list'),
            data={'text': 'Text', 'task': task.id, 'student': student.id},
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 201

    def test_create_solution_professor(self):
        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.professor.set([professor])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name="Задача_1", text="Текст задачи_1", start_time=today, finish_time=today + delta, course=course
        )
        course.refresh_from_db()

        response = self.client.post(
            reverse('solution-list'),
            data={'text': 'Text', 'task': task.id, 'student': professor.id},
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 403

    def test_get_solutions_professor(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.professor.set([professor])
        course.groups.set([group])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name="Задача_1", text="Текст задачи_1", start_time=today, finish_time=today + delta, course=course
        )
        solution = Solution.objects.create(
            text='Text',
            task=task,
            student=student
        )

        solution.refresh_from_db()
        task.refresh_from_db()
        course.refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.get(
            reverse('solution-list'),
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        assert response.status_code == 200
        assert response.json().get('count') == 1
        assert response.json().get('results')[0]['id'] == solution.id

    def test_get_solutions_professor(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.groups.set([group])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name="Задача_1", text="Текст задачи_1", start_time=today, finish_time=today + delta, course=course
        )

        solution = Solution.objects.create(text='Text', task=task, student=student)

        solution.refresh_from_db()
        task.refresh_from_db()
        course.refresh_from_db()
        student.refresh_from_db()

        response = self.client.get(
            reverse('solution-list'),
            **{'HTTP_X_SECRET_KEY': student.secret_key}
        )

        assert response.status_code == 200
        assert response.json().get('count') == 1
        assert response.json().get('results')[0]['id'] == solution.id
