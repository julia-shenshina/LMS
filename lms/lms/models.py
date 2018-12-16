from django.db import models
from django.conf import settings
from uuid import uuid4

from lms.validators import phone_number_validation


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    token = models.CharField(max_length=64,
                             default=uuid4,
                             null=True,
                             unique=True,
                             blank=True)
    email = models.EmailField(max_length=128,
                              blank=True,
                              null=True,
                              unique=True)
    phone = models.CharField(max_length=12,
                             validators=[phone_number_validation],
                             blank=True,
                             null=True,
                             unique=True)
    password = models.CharField(max_length=64, null=True, blank=True)
    secret_key = models.CharField(max_length=64, null=True, blank=True)
    vk_link = models.CharField(max_length=64,
                               default="",
                               blank=True)
    fb_link = models.CharField(max_length=64,
                               default="",
                               blank=True)
    linkedin_link = models.CharField(max_length=64,
                                     default="",
                                     blank=True)
    insta_link = models.CharField(max_length=64,
                                  default="",
                                  blank=True)

    class Meta:
        abstract = True


class Professor(Person):
    pass


class Student(Person):
    group = models.ForeignKey('Group',
                              on_delete=models.CASCADE,
                              related_name='students',
                              null=True)
    start_year = models.IntegerField(choices=settings.START_STUDY_YEARS)
    degree = models.CharField(max_length=64,
                              choices=settings.DEGREES)
    study_form = models.CharField(max_length=64,
                                  choices=settings.STUDY_FORMS)
    study_base = models.CharField(max_length=64,
                                  choices=settings.STUDY_BASES)


class Faculty(models.Model):
    name = models.CharField(max_length=64,
                            unique=True)


class Group(models.Model):
    name = models.CharField(max_length=64,
                            unique=True)
    faculty = models.ForeignKey('Faculty',
                                on_delete=models.SET_NULL,
                                related_name='groups',
                                null=True)
    level = models.IntegerField(choices=settings.STUDY_LEVEL)


class Course(models.Model):
    name = models.CharField(max_length=64,
                            unique=True)
    description = models.CharField(max_length=512)
    professor = models.ManyToManyField('Professor',
                                       related_name="courses",
                                       blank=True,
                                       null=True)
    groups = models.ManyToManyField('Group',
                                    related_name="courses",
                                    blank=True,
                                    null=True)
    headmen = models.ManyToManyField("Student", related_name="driven_courses", blank=True)


class Material(models.Model):
    name = models.CharField(max_length=128)
    text = models.CharField(max_length=512)
    updated_at = models.DateField(auto_now=True)
    course = models.ForeignKey("Course", related_name="materials", on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=128)
    text = models.CharField(max_length=512)
    start_time = models.DateField()
    finish_time = models.DateField()
    course = models.ForeignKey("Course", related_name="tasks", on_delete=models.CASCADE)


class Solution(models.Model):
    student = models.ForeignKey("Student", related_name="solutions", on_delete=models.CASCADE)
    task = models.ForeignKey("Task", related_name="solutions", on_delete=models.CASCADE)
    text = models.CharField(max_length=512)