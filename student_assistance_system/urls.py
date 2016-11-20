from django.conf.urls import url
import django.contrib.auth.views as auth_views

from views import *

app_name = 'student_assistance_system'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^schedules/(?P<schedule_id>[0-9]+)/$', ViewScheduleView.as_view(), name='view_schedule'),
    url(r'^schedules/(?P<schedule_id>[0-9]+)/edit/$', EditScheduleView.as_view(), name='edit_schedule'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^search', SearchView.as_view()),
    url(r'^results', SearchResultsView.as_view(), name='courses'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout')
]
