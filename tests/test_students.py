from rest_framework.test import APITestCase
from django.urls import reverse

from lms.models.models import Faculty, Group, Student, Professor, Course


class TestStudent(APITestCase):
    def test_get_students_student(self):
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

    def test_get_students_professor(self):
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
                first_name="first", last_name="last", group=groups[1], secret_key="2", start_year=2017
            )
        ]
        professor = Professor.objects.create(
            first_name='second', last_name='second', secret_key="3"
        )
        course = Course.objects.create(name='Курс_1', description="Описание курса_1")
        course.professor.set([professor])
        course.groups.set([groups[0]])

        course.refresh_from_db()
        for group in groups:
            group.refresh_from_db()
        for student in students:
            student.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.get(
            reverse('student-list'),
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 200
        assert response.json()['count'] == 1
        assert response.json()['results'][0]['id'] == students[0].id

    def test_get_other_student_profile(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)
        students = [
            Student.objects.create(
                first_name="first", last_name="last", group=group, secret_key="1", start_year=2017, study_base="bg"
            ),
            Student.objects.create(
                first_name="first", last_name="last", group=group, secret_key="2", start_year=2017, study_base="bg"
            )
        ]

        response = self.client.get(
            reverse('student-detail', args=[students[1].id]),
            **{"HTTP_X_SECRET_KEY": students[0].secret_key}
        )

        assert response.status_code == 200
        assert 'study_base' not in response.json()

    def test_get_other_student_profile(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)
        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="1", start_year=2017, study_base="bg"
        )

        response = self.client.get(
            reverse('student-detail', args=[student.id]),
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 200
        assert 'study_base' in response.json()

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
