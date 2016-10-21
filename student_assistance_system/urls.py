from django.conf.urls import include, url

from . import views

app_name = 'student_assistance_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
