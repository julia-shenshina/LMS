import re

from django.core.exceptions import ValidationError


def phone_number_validation(phone_number):
    if phone_number:
        regex = re.compile(r"^\+?1?\d{9,15}$")
        assert regex.fullmatch(phone_number), ValidationError(message="Wrong phone number")


def insta_link_validation(link):
    if link:
        pattern = r'https://www.instagram.com/*'
        assert re.match(pattern, link)


def fb_link_validation(link):
    if link:
        pattern = r'https://www.facebook.com/*'
        assert re.match(pattern, link)


def linkedin_link_validation(link):
    if link:
        pattern = r'https://linkedin.com/*'
        assert re.match(pattern, link)


def vk_link_validation(link):
    if link:
        pattern = r'https://vk.com/*'
        assert re.match(pattern, link)
