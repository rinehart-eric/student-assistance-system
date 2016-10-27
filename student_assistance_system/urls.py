from django.conf.urls import url
import django.contrib.auth.views as auth_views

from . import views

app_name = 'student_assistance_system'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^schedules/(?P<schedule_id>[0-9]+)/$', views.view_schedule, name='view_schedule'),
    url(r'^schedules/(?P<schedule_id>[0-9]+)/edit/$', views.edit_schedule, name='edit_schedule'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
]
