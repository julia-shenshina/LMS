from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied

from lms.api.utils import get_student_or_professor


class LMSAuthentication(BaseAuthentication):
    def authenticate(self, request):
        secret_key = request.META.get('HTTP_X_SECRET_KEY')
        if secret_key is None:
            raise AuthenticationFailed()

        person = get_student_or_professor(secret_key=secret_key)
        if person is None:
            raise PermissionDenied()

        return person, secret_key
