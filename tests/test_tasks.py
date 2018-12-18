from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from lms.models import Course, Faculty, Group, Professor, Student, Task


class TestSolution(APITestCase):
    def test_get_tasks_professor(self):
        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        courses = [
            Course.objects.create(name="Курс_1", description="Описание курса_1"),
            Course.objects.create(name="Курс_2", description="Описание курса_2")
        ]
        courses[0].professor.set([professor])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        tasks = [
            Task.objects.create(
                name="Задача_1", text="Текст задачи_1", start_time=today, finish_time=today + delta, course=courses[0]
            ),
            Task.objects.create(
                name="Задача_2", text="Текст задачи_2", start_time=today, finish_time=today + delta, course=courses[1]
            )
        ]

        for course, task in zip(courses, tasks):
            task.refresh_from_db()
            course.refresh_from_db()

        professor.refresh_from_db()

        response = self.client.get(
            reverse('task-list'),
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 200
        assert response.json().get("count") == 1
        assert response.json().get("results")[0]["id"] == tasks[0].id

    def test_get_tasks_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        courses = [
            Course.objects.create(name="Курс_1", description="Описание курса_1"),
            Course.objects.create(name="Курс_2", description="Описание курса_2")
        ]
        courses[0].groups.set([group])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        tasks = [
            Task.objects.create(
                name="Задача_1", text="Текст задачи_1", start_time=today, finish_time=today + delta, course=courses[0]
            ),
            Task.objects.create(
                name="Задача_3", text="Текст задачи_3", start_time=today - 2 * delta, finish_time=today - delta, course=courses[0]
            ),
            Task.objects.create(
                name="Задача_2", text="Текст задачи_2", start_time=today + delta, finish_time=today + 2 * delta, course=courses[0]
            ),
            Task.objects.create(
                name="Задача_1", text="Текст задачи_1", start_time=today, finish_time=today + delta, course=courses[1]
            ),
        ]

        for course in courses:
            course.refresh_from_db()

        for task in tasks:
            task.refresh_from_db()

        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.get(
            reverse('task-list'),
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 200
        assert response.json().get("count") == 1
        assert response.json().get("results")[0]["id"] == tasks[0].id

    def test_create_tasks_professor_ok(self):
        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        course = Course.objects.create(name='Курс_1', description='Описание курса_1')
        course.professor.set([professor])

        course.refresh_from_db()
        professor.refresh_from_db()

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)

        response = self.client.post(
            reverse('task-list'),
            data={
                     'name': 'Задание от профессора',
                     'text': 'Текст задания от профессора',
                     'start_time': today,
                     'finish_time': today + delta,
                     'course': course.id
                 },
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 201

    def test_create_tasks_professor_failed(self):
        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        course = Course.objects.create(name='Курс_1', description='Описание курса_1')

        course.refresh_from_db()
        professor.refresh_from_db()

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)

        response = self.client.post(
            reverse('task-list'),
            data={
                     'name': 'Задание от профессора',
                     'text': 'Текст задания от профессора',
                     'start_time': today,
                     'finish_time': today + delta,
                     'course': course.id
                 },
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 403

    def test_create_tasks_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name='Курс_1', description='Описание курса_1')

        course.refresh_from_db()
        student.refresh_from_db()

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)

        response = self.client.post(
            reverse('task-list'),
            data={
                     'name': 'Задание от профессора',
                     'text': 'Текст задания от профессора',
                     'start_time': today,
                     'finish_time': today + delta,
                     'course': course.id
                 },
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 403

    def test_delete_task_professor(self):
        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        course = Course.objects.create(name='Курс_1', description='Описание курса_1')
        course.professor.set([professor])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name='Задание', start_time=today, finish_time=today + delta, course=course
        )

        task.refresh_from_db()
        course.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.delete(
            reverse('task-detail', args=[task.id]),
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 204

    def test_delete_tasks_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name='Курс_1', description='Описание курса_1')
        course.groups.set([group])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name='Задание', start_time=today, finish_time=today + delta, course=course
        )

        task.refresh_from_db()
        course.refresh_from_db()
        student.refresh_from_db()

        response = self.client.delete(
            reverse('task-detail', args=[task.id]),
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 403

    def test_update_task_professor_ok(self):
        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        course = Course.objects.create(name='Курс_1', description='Описание курса_1')
        course.professor.set([professor])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name='Задание', start_time=today, finish_time=today + delta, course=course
        )

        task.refresh_from_db()
        course.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.patch(
            reverse('task-detail', args=[task.id]),
            data={'name': 'New name'},
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 200

    def test_update_task_professor_failed(self):
        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        course = Course.objects.create(name='Курс_1', description='Описание курса_1')

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name='Задание', start_time=today, finish_time=today + delta, course=course
        )

        task.refresh_from_db()
        course.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.patch(
            reverse('task-detail', args=[task.id]),
            data={'name': 'New name'},
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 404

    def test_update_tasks_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name='Курс_1', description='Описание курса_1')
        course.groups.set([group])

        today = timezone.now().date()
        delta = timezone.timedelta(days=3)
        task = Task.objects.create(
            name='Задание', start_time=today, finish_time=today + delta, course=course
        )

        task.refresh_from_db()
        course.refresh_from_db()
        student.refresh_from_db()

        response = self.client.patch(
            reverse('task-detail', args=[task.id]),
            data={'name': 'New name'},
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 403
