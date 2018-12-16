from lms.models import Student


def can_edit_student_profile(requester, object):
    return requester == object


def can_edit_professor_profile(requester, object):
    return requester == object


def can_view_study_base(requester, object):
    return requester == object


def can_edit_course_materials(requester, course):
    return requester in course.professor.all() or requester in course.headmen.all()


def can_delete_course_materials(requester, course):
    return requester in course.professor.all() or requester in course.headmen.all()


def can_create_course_materials(requester, course):
    return requester in course.professor.all() or requester in course.headmen.all()


def can_edit_course_tasks(requester, course):
    return requester in course.professor.all()


def can_submit_solution(requester):
    return isinstance(requester, Student)
