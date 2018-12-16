from lms.models import Student, Professor


def get_student_or_professor(**params):
    person = Student.objects.filter(**params).first() or Professor.objects.filter(**params).first()
    return person
