from rest_framework.test import APITestCase
from django.urls import reverse

from lms.models.models import Course, Faculty, Group, Professor, Student


class TestCourses(APITestCase):
    def test_read_course_professor(self):
        professor = Professor.objects.create(first_name='first', last_name='last', secret_key="123123")

        courses = [
            Course.objects.create(name="Курс_1", description="Описание курса_1"),
            Course.objects.create(name="Курс_2", description="Описание курса_2")
        ]
        courses[0].professor.set([professor])

        professor.refresh_from_db()
        courses[0].refresh_from_db()

        response = self.client.get(
            reverse('course-list'),
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 200
        assert response.json().get('count') == 1
        assert response.json().get('results')[0]["id"] == courses[0].id

    def test_read_courses_student(self):
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

        courses[0].refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.get(
            reverse('course-list'),
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 200
        assert response.json().get('count') == 1
        assert response.json().get('results')[0]["id"] == courses[0].id

    def test_enroll_group(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        groups = [
            Group.objects.create(name="Группа_1", faculty=faculty, level=1),
            Group.objects.create(name="Группа_2", faculty=faculty, level=1)
        ]

        student = Student.objects.create(
            first_name="first", last_name="last", group=groups[0], secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс_1", description="Описание курса_1")
        course.groups.set([groups[0]])

        response = self.client.get(
            reverse('course-list'),
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 200
        assert response.json().get('count') == 1
        assert len(response.json().get('results')[0]["groups"]) == 1
        assert response.json().get('results')[0]["groups"][0] == groups[0].id

    def test_add_headmen_ok(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name='Группа_1', faculty=faculty, level=1)
        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        professor = Professor.objects.create(
            first_name='first_prof', last_name='last_prof', secret_key="456456"
        )
        course = Course.objects.create(name="Курс_1", description="Описание курса_1")
        course.groups.set([group])
        course.professor.set([professor])

        course.refresh_from_db()
        student.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.patch(
            reverse('course-detail', args=[course.id]),
            data={'headmen': [student.id]},
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        assert response.status_code == 200

    def test_add_headmen_failed(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name='Группа_1', faculty=faculty, level=1)
        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        professor = Professor.objects.create(
            first_name='first_prof', last_name='last_prof', secret_key="456456"
        )
        course = Course.objects.create(name="Курс_1", description="Описание курса_1")
        course.professor.set([professor])

        course.refresh_from_db()
        student.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.patch(
            reverse('course-detail', args=[course.id]),
            data={'headmen': [student.id]},
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        assert response.status_code == 400

    def test_add_headmen_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name='Группа_1', faculty=faculty, level=1)
        students = [
            Student.objects.create(
                first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
            ),
            Student.objects.create(
                first_name="second", last_name="last", group=group, secret_key="567567", start_year=2017
            )
        ]

        course = Course.objects.create(name="Курс_1", description="Описание курса_1")
        course.groups.set([group])
        course.headmen.set([students[0]])

        course.refresh_from_db()
        for student in students:
            student.refresh_from_db()

        response = self.client.patch(
            reverse('course-detail', args=[course.id]),
            data={'headmen': [students[1].id]},
            **{'HTTP_X_SECRET_KEY': students[0].secret_key}
        )

        assert response.status_code == 403
