from django.conf.urls import url
import django.contrib.auth.views as auth_views

from views import *

app_name = 'student_assistance_system'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^schedules/(?P<schedule_id>[0-9]+)/$', ViewScheduleView.as_view(), {'editing': False}, name='view_schedule'),
    url(r'^schedules/(?P<schedule_id>[0-9]+)/edit/$', ViewScheduleView.as_view(), {'editing': True}, name='edit_schedule'),
    url(r'^schedules/edit/remove/$', RemoveSectionScheduleView.as_view(), {'editing': True}, name='remove_section'),
    url(r'^schedules/section/add$', AddSectionScheduleView.as_view(), {'editing': True}, name='add_section'),
    url(r'^sections/(?P<section_id>[0-9]+)/$', ViewSectionView.as_view(), name='view_section'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^search', SearchView.as_view(), name='search'),
    url(r'^results', SearchResultsView.as_view(), name='courses'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout')
]
