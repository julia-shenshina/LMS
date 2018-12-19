from rest_framework.test import APITestCase
from django.urls import reverse

from lms.models.models import Faculty, Group, Professor, Student


class TestProfessor(APITestCase):
    def test_read_professors_professor(self):
        professor = Professor.objects.create(
            first_name='first', last_name='last', secret_key='123123'
        )
        response = self.client.get(
            reverse('professor-list'),
            **{"HTTP_X_SECRET_KEY": professor.secret_key}
        )

        assert response.status_code == 200
        assert response.json()['count'] == 1
        assert response.json()['results'][0]['id'] == professor.id

    def test_read_professors_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)
        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        group.refresh_from_db()
        student.refresh_from_db()

        professor = Professor.objects.create(
            first_name='first', last_name='last', secret_key='456456'
        )
        response = self.client.get(
            reverse('professor-list'),
            **{"HTTP_X_SECRET_KEY": student.secret_key}
        )

        assert response.status_code == 200
        assert response.json()['count'] == 1
        assert response.json()['results'][0]['id'] == professor.id

    def test_update_professor_ok(self):
        professor = Professor.objects.create(
            first_name="first", last_name="last", secret_key="123123"
        )

        phone = '+79569569568'
        response = self.client.patch(
            reverse('professor-detail', args=[professor.id]),
            data={'phone': phone},
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        professor.refresh_from_db()

        assert response.status_code == 200
        assert professor.phone == phone

    def test_update_professor_failed(self):
        professors = [
            Professor.objects.create(
                first_name='first', last_name='last', secret_key='123123'
            ),
            Professor.objects.create(
                first_name='second', last_name='last', secret_key='456456'
            )
        ]

        phone = '+79569569568'
        response = self.client.patch(
            reverse('professor-detail', args=[professors[0].id]),
            data={'phone': phone},
            **{'HTTP_X_SECRET_KEY': professors[1].secret_key}
        )

        assert response.status_code == 403
