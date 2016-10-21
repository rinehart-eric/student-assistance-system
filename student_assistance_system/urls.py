from django.conf.urls import include, url
import django.contrib.auth.views as auth_views

from . import views

app_name = 'student_assistance_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/profile/', views.profile, name='profile'),
    url(r'^accounts/login/', auth_views.login, name='login'),
    url(r'^accounts/logout/', auth_views.logout, name='logout'),
]
