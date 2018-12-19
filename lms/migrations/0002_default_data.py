# Generated by Django 2.1.4 on 2018-12-19 19:49

from django.db import migrations
from django.utils import timezone


def create_default_faculties(apps):
    Faculty = apps.get_model('lms', 'Faculty')
    faculties = []
    for i in range(2):
        faculties.append(Faculty.objects.create(name='Факультет_%s' % (i + 1)))
    return faculties


def create_default_groups(apps, faculties):
    Group = apps.get_model('lms', 'Group')
    groups = []
    for j, faculty in enumerate(faculties):
        for i in range(2):
            groups.append(Group.objects.create(name='Группа_%s%s' % (i + 1, j + 1), level=1, faculty=faculty))
    return groups


def create_default_professors(apps):
    Professor = apps.get_model('lms', 'Professor')
    professors = [
        Professor.objects.create(
            first_name='Katy', last_name='Perry', insta_link='https://www.instagram.com/katyperry/',
            email='katy@perry.com', password='12345678'
        ),
        Professor.objects.create(
            first_name='Профессор', last_name='Профессорович', phone='89000000000'
        )
    ]
    return professors


def create_default_courses(apps):
    Course = apps.get_model('lms', 'Course')
    courses = []
    for i in range(3):
        courses.append(Course.objects.create(name='Курс_%s' % (i + 1), description='Описание курса_%s' % (i + 1)))
    return courses


def create_default_students(apps, groups):
    Student = apps.get_model('lms', 'Student')
    students = []
    for i, group in enumerate(groups):
        current = []
        for j in range(2):
            email = "aaa@example.com" if i == 0 and j == 0 else None
            password = "qwertyqwerty" if i == 0 and j == 0 else None
            current.append(Student.objects.create(
                first_name='Имя_%s%s' % (i + 1, j + 1), last_name='Фамилия_%s%s' % (i + 1, j + 1), group=group,
                start_year=2018, email=email, password=password
            ))
        students.append(current)
    return students


def create_default_materials(apps, courses):
    Materials = apps.get_model('lms', 'Material')
    materials = []
    for j, course in enumerate(courses):
        current = []
        for i in range(2):
            current.append(Materials.objects.create(name='Материал_%s%s' % (i + 1, j + 1), course=course))
        materials.append(current)
    return materials


def create_default_tasks(apps, courses):
    Task = apps.get_model('lms', 'Task')
    tasks = []
    today = timezone.now().today()
    delta = timezone.timedelta(days=14)
    for i, course in enumerate(courses):
        tasks.append(
            [
                Task.objects.create(
                    name='Задание_%s_1' % (i + 1), start_time=today, finish_time=today + delta, course=course
                ),
                Task.objects.create(
                    name='Задание_%s_2' % (i + 1), start_time=today - delta, finish_time=today + 2 * delta, course=course
                )
            ]
        )
    return tasks


def create_default_solution(apps, student, task):
    Solution = apps.get_model('lms', 'Solution')
    return Solution.objects.create(text='Текст решения', student=student, task=task)


def create_default_data(apps, schema_editor):
    faculties = create_default_faculties(apps)
    groups = create_default_groups(apps, faculties)
    professors = create_default_professors(apps)
    courses = create_default_courses(apps)

    for i, course in enumerate(courses):
        groups[1].courses.set([course])
        if i % 2:
            course.professor.set([professors[0]])
        if i < 2:
            course.professor.set([professors[1]])
            groups[0].courses.set([course])

    students = create_default_students(apps, groups)
    courses[0].headmen.set(students[0])

    tasks = create_default_tasks(apps, courses)
    materials = create_default_materials(apps, courses)

    create_default_solution(apps, students[0][0], tasks[0][0])
    create_default_solution(apps, students[1][0], tasks[1][1])


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_data)
    ]
