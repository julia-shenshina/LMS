from rest_framework.test import APITestCase

from lms.models import Course, Faculty, Group, Professor, Student


class TestCourses(APITestCase):
    def test_read_course_professor(self):
        professor = Professor.objects.create(first_name='first', last_name='last')

        courses = [
            Course.objects.create(name="Курс_1", description="Описание курса_1"),
            Course.objects.create(name="Курс_2", description="Описание курса_2")
        ]
        courses[0].professor.set([professor])

        professor.refresh_from_db()
        courses[0].refresh_from_db()

        assert len(professor.courses.all()) == 1
        assert professor.courses.first().id == courses[0].id

        assert len(courses[0].professor.all()) == 1
        assert courses[0].professor.first().id == professor.id

        assert len(courses[1].professor.all()) == 0

    def test_read_courses_student(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        group = Group.objects.create(name="Группа_1", faculty=faculty, level=1)
        student = Student.objects.create(first_name="first", last_name="last", group=group, start_year=2017)

        courses = [
            Course.objects.create(name="Курс_1", description="Описание курса_1"),
            Course.objects.create(name="Курс_2", description="Описание курса_2")
        ]
        courses[0].groups.set([group])

        courses[0].refresh_from_db()
        group.refresh_from_db()
        student.refresh_from_db()

        assert len(student.group.courses.all()) == 1
        assert student.group.courses.first() == courses[0]

    def test_enroll_group(self):
        faculty = Faculty.objects.create(name="Факультет_1")
        groups = [
            Group.objects.create(name="Группа_1", faculty=faculty, level=1),
            Group.objects.create(name="Группа_2", faculty=faculty, level=1)
        ]

        course = Course.objects.create(name="Курс_1", description="Описание курса_1")
        course.groups.set([groups[0]])

        assert len(course.groups.all()) == 1
        assert course.groups.first() == groups[0]

        assert len(groups[0].courses.all()) == 1
        assert groups[0].courses.first() == course

        assert len(groups[1].courses.all()) == 0
