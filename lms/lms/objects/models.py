from django.db import models
from django.conf import settings

from lms.objects.validation import phone_number_validation


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Professor(Person):
    class ProfessorMeta(Person.Meta):
        db_table = 'professor_info'


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    group = models.ForeignKey('Group',
                              on_delete=models.CASCADE,
                              related_name='students',
                              null=True)
    start_year = models.IntegerField(choices=settings.START_STUDY_YEARS)
    degree = models.CharField(max_length=50,
                              choices=settings.DEGREES)
    study_form = models.CharField(max_length=50,
                                  choices=settings.STUDY_FORMS)
    study_base = models.CharField(max_length=50,
                                  choices=settings.STUDY_BASES)
    email = models.EmailField(max_length=100,
                              blank=True,
                              null=True,
                              unique=True)
    phone = models.CharField(max_length=12,
                             validators=[phone_number_validation],
                             blank=True,
                             null=True,
                             unique=True)

    class StudentMeta(Person.Meta):
        db_table = "student_info"


class Faculty(models.Model):
    name = models.CharField(max_length=50,
                            unique=True)


class Group(models.Model):
    name = models.CharField(max_length=50,
                            unique=True)
    faculty = models.ForeignKey('Faculty',
                                on_delete=models.SET_NULL,
                                related_name='groups',
                                null=True)
    level = models.IntegerField()


class Course(models.Model):
    name = models.CharField(max_length=50,
                            unique=True)
    description = models.CharField(max_length=500)
    professor = models.ForeignKey('Professor',
                                  on_delete=models.SET_NULL,
                                  related_name="courses",
                                  blank=True,
                                  null=True)
    groups = models.ManyToManyField('Group',
                                    related_name="courses",
                                    blank=True,
                                    null=True)
