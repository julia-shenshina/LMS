import pdb

from django.urls import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Faculty, Group, Professor, Student, Material


class TestMaterials(APITestCase):
    def test_read_materials_professor(self):
        professor = Professor.objects.create(first_name='first', last_name='last')

        courses = [
            Course.objects.create(name="Курс_1", description="Описание курса_1"),
            Course.objects.create(name="Курс_2", description="Описание курса_2")
        ]

        materials = [
            Material.objects.create(name="Учебник по курсу_1", text="text_1", course=courses[0]),
            Material.objects.create(name="Учебник по курсу_2", text="text_2", course=courses[1])
        ]
        courses[0].professor.set([professor])

        for course in courses:
            course.refresh_from_db()

        assert len(professor.courses.first().materials.all()) == 1
        assert professor.courses.first().materials.first() == courses[0].materials.first()

    def test_read_materials_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)
        student = Student.objects.create(
            first_name="first", last_name="last", group=group, start_year=2016
        )

        courses = [
            Course.objects.create(name="Курс_1", description="Описание курса_1"),
            Course.objects.create(name="Курс_2", description="Описание курса_2")
        ]

        materials = [
            Material.objects.create(name="Учебник по курсу_1", text="text_1", course=courses[0]),
            Material.objects.create(name="Учебник по курсу_2", text="text_2", course=courses[1])
        ]

        group.courses.set([courses[0]])

        for course, material in zip(courses, materials):
            course.materials.set([material])
            course.refresh_from_db()

        group.refresh_from_db()
        student.refresh_from_db()

        assert len(student.group.courses.first().materials.all()) == 1
        assert student.group.courses.first().materials.first() == materials[0]

    def test_update_materials_professor_ok(self):
        professor = Professor.objects.create(
            first_name='first', last_name='last', secret_key="123123"
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.professor.set([professor])

        material = Material.objects.create(name="Учебник по курсу", text="text", course=course)

        material.refresh_from_db()
        course.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.patch(
            reverse('material-detail', args=[material.id]),
            data={'text': 'Текст учебника по курсу'},
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        assert response.status_code == 200

    def test_update_materials_professor_failed(self):
        professor = Professor.objects.create(
            first_name='first', last_name='last', secret_key="123123"
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        material = Material.objects.create(name="Учебник по курсу", text="text", course=course)

        material.refresh_from_db()
        course.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.patch(
            reverse('material-detail', args=[material.id]),
            data={'text': 'Текст учебника по курсу'},
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        assert response.status_code == 404

    def test_update_materials_student_failed(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.groups.set([group])
        material = Material.objects.create(name="Учебник по курсу", text="text", course=course)

        material.refresh_from_db()
        course.refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.patch(
            reverse('material-detail', args=[material.id]),
            data={'text': 'Текст учебника по курсу'},
            **{'HTTP_X_SECRET_KEY': student.secret_key}
        )

        assert response.status_code == 403

    def test_update_materials_student_ok(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.groups.set([group])
        course.headmen.set([student])
        material = Material.objects.create(name="Учебник по курсу", text="text", course=course)

        material.refresh_from_db()
        course.refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.patch(
            reverse('material-detail', args=[material.id]),
            data={'text': 'Текст учебника по курсу'},
            **{'HTTP_X_SECRET_KEY': student.secret_key}
        )

        assert response.status_code == 200

    def test_delete_materials_professor(self):
        professor = Professor.objects.create(
            first_name='first', last_name='last', secret_key="123123"
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.professor.set([professor])

        material = Material.objects.create(name="Учебник по курсу", text="text", course=course)

        material.refresh_from_db()
        course.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.delete(
            reverse('material-detail', args=[material.id]),
            data={'text': 'Текст учебника по курсу'},
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        assert response.status_code == 204

    def test_delete_materials_student_ok(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.groups.set([group])
        course.headmen.set([student])
        material = Material.objects.create(name="Учебник по курсу", text="text", course=course)

        material.refresh_from_db()
        course.refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.delete(
            reverse('material-detail', args=[material.id]),
            data={'text': 'Текст учебника по курсу'},
            **{'HTTP_X_SECRET_KEY': student.secret_key}
        )

        assert response.status_code == 204

    def test_delete_materials_student_failed(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        email = "aaa@example.com"
        password = "password"
        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.groups.set([group])
        material = Material.objects.create(name="Учебник по курсу", text="text", course=course)

        material.refresh_from_db()
        course.refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.delete(
            reverse('material-detail', args=[material.id]),
            data={'text': 'Текст учебника по курсу'},
            **{'HTTP_X_SECRET_KEY': student.secret_key}
        )

        assert response.status_code == 403

    def test_create_materials_student_ok(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.groups.set([group])
        course.headmen.set([student])

        course.refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.post(
            reverse('material-list'),
            data={'name': 'Новые материалы', 'text': 'Текст учебника по курсу', 'course': course.id},
            **{'HTTP_X_SECRET_KEY': student.secret_key}
        )

        assert response.status_code == 201

    def test_create_materials_student_failed(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)

        student = Student.objects.create(
            first_name="first", last_name="last", group=group, secret_key="123123", start_year=2017
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.groups.set([group])

        course.refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        response = self.client.post(
            reverse('material-list'),
            data={'name': 'Новые материалы', 'text': 'Текст учебника по курсу', 'course': course.id},
            **{'HTTP_X_SECRET_KEY': student.secret_key}
        )

        assert response.status_code == 403

    def test_create_materials_professor_ok(self):
        professor = Professor.objects.create(
            first_name='first', last_name='last', secret_key="123123"
        )

        course = Course.objects.create(name="Курс", description="Описание курса")
        course.professor.set([professor])

        course.refresh_from_db()
        professor.refresh_from_db()

        response = self.client.post(
            reverse('material-list'),
            data={'name': 'Новые материалы', 'text': 'Текст учебника по курсу', 'course': course.id},
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        assert response.status_code == 201

    def test_update_materials_professor_failed(self):
        professor = Professor.objects.create(
            first_name='first', last_name='last', secret_key="123123"
        )

        course = Course.objects.create(name="Курс", description="Описание курса")

        response = self.client.post(
            reverse('material-list'),
            data={'name': 'Новые материалы', 'text': 'Текст учебника по курсу', 'course': course.id},
            **{'HTTP_X_SECRET_KEY': professor.secret_key}
        )

        assert response.status_code == 403
