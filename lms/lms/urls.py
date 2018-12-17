from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from lms.api import views

router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'faculties', views.FacultyViewSet, basename='faculty')
router.register(r'professors', views.ProfessorViewSet, basename='professor')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'materials', views.MaterialViewSet, basename='material')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'solutions', views.SolutionViewSet, basename='solution')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'admin/', admin.site.urls),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^login/$', views.LoginView.as_view(), name='login')
]
