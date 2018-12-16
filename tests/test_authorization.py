from django.urls import reverse
from rest_framework.test import APITestCase

from lms.models import Professor


class TestAuth(APITestCase):
    def test_registration(self):
        professor = Professor.objects.create(first_name='first', last_name='last')
        registration_token = professor.token
        assert registration_token is not None
        email = 'aaa@email.com'
        password = 'password'

        response = self.client.post(
            reverse('registration'),
            data={'token': registration_token, 'email': email, 'password': password}
        )
        assert response.status_code == 200
        assert response.json() == 'ok'

        professor.refresh_from_db()
        assert professor.token is None
        assert professor.email == email
        assert professor.password == password

    def test_login(self):
        email = 'aaa@email.com'
        password = 'password'

        professor = Professor.objects.create(
            first_name='first', last_name='last', email=email, password=password
        )
        response = self.client.post(
            reverse('login'),
            data={'email': email, 'password': password}
        )
        assert response.status_code == 200
        professor.refresh_from_db()
        assert response.json() == {'secret_key': professor.secret_key}
