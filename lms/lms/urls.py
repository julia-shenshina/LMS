from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from lms.objects import views


router = routers.DefaultRouter()
router.register(r'users', views.StudentViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'faculty', views.FacultyViewSet)
router.register(r'professor', views.ProfessorViewSet)
router.register(r'course', views.CourseViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'admin/', admin.site.urls)
]