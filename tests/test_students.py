from rest_framework.test import APITestCase
from django.urls import reverse

from lms.models import Course, Faculty, Group, Professor, Student


class TestStudent(APITestCase):
    def test_read_students(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        groups = [
            Group.objects.create(name="Группа_1", faculty=faculty, level=1),
            Group.objects.create(name="Группа_2", faculty=faculty, level=1)
        ]
        students = [
            Student.objects.create(
                first_name="first", last_name="last", group=groups[0], secret_key="1", start_year=2017
            ),
            Student.objects.create(
                first_name="first", last_name="last", group=groups[0], secret_key="2", start_year=2017
            ),
            Student.objects.create(
                first_name="first", last_name="last", group=groups[1], secret_key="3", start_year=2017
            )
        ]

        for group in groups:
            group.refresh_from_db()
        for student in students:
            student.refresh_from_db()

        response = self.client.get(
            reverse('student-list'),
            **{"HTTP_X_SECRET_KEY": students[0].secret_key}
        )

        assert response.status_code == 200
        assert response.json().get('count') == 2
        assert response.json().get('results')[0]['id'] == students[0].id
        assert response.json().get('results')[1]['id'] == students[1].id

    def test_update_student_ok(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)
        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        group.refresh_from_db()
        student.refresh_from_db()

        phone = '+79569569568'
        response = self.client.patch(
            reverse('student-detail', args=[student.id]),
            data={'phone': phone},
            **{'HTTP_X_SECRET_KEY': student.secret_key}
        )

        student.refresh_from_db()

        assert response.status_code == 200
        assert student.phone == phone

    def test_update_student_failed(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)
        students = [
            Student.objects.create(
                first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
            ),
            Student.objects.create(
                first_name="first", last_name="last", group=group, secret_key="456456", start_year=2017
            )
        ]

        group.refresh_from_db()
        for student in students:
            student.refresh_from_db()

        phone = '+79569569568'
        response = self.client.patch(
            reverse('student-detail', args=[students[1].id]),
            data={'phone': phone},
            **{'HTTP_X_SECRET_KEY': students[0].secret_key}
        )

        assert response.status_code == 403
