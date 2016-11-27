from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Section


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    template_name = 'student_assistance_system/index.html'

    def get_requirement_sets(self, p):
        majors_and_concentrations = [[um.major, um.concentration] for um in p.usermajor_set.all()]
        filtered = [reqs for pair in majors_and_concentrations for reqs in pair if reqs is not None]
        return filtered + list(p.minors.all())

    def get(self, request, *args, **kwargs):
        p = request.user.profile
        schedules = request.user.profile.schedule_set.all()
        req_sets = self.get_requirement_sets(p)
        most_recently_updated_schedule = max(schedules, key=lambda s: s.updated) if schedules else None

        return render(request, self.template_name, dict(schedule=most_recently_updated_schedule, req_sets=req_sets))


@method_decorator(login_required, name='dispatch')
class SearchView(View):
    template_name = 'student_assistance_system/search.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class SearchResultsView(generic.ListView):
    model = Section
    template_name = 'student_assistance_system/search_results.html'
    context_object_name = "sections"
    paginate_by = 10

    def filter_by_name(self, request, sections):
        name = request.get('name')
        if name:
            return sections.filter(Q(course__name__icontains=name))
        return sections

    def filter_by_professor(self, request, sections):
        professor = request.get('prof')
        if professor:
            return sections.filter(Q(professor__icontains=professor))
        return sections

    def determine_course_number(self, course):
        if not course[-1].isdigit():
            course = course[0:len(course)-1]
        return int(course) if course.isdigit() else 999

    def determine_course_letter(self, course):
        if course[-1].isdigit():
            return "0"
        return course[-1].upper()

    def determine_courses_in_range(self, upper_number, lower_number, sections):
        lower_course_letter = self.determine_course_letter(lower_number)
        upper_course_letter = self.determine_course_letter(upper_number)
        lower_course_number = self.determine_course_number(lower_number)
        upper_course_number = self.determine_course_number(upper_number)
        sections_in_range = []
        for section in sections:
                section_number = self.determine_course_number(section.course.course_number)
                section_letter = self.determine_course_letter(section.course.course_number)
                if lower_course_number < section_number < upper_course_number:
                    sections_in_range.append(section)
                elif lower_course_number == section_number and section_letter >= lower_course_letter:
                    sections_in_range.append(section)
                elif upper_course_number == section_number and section_letter <= upper_course_letter:
                    sections_in_range.append(section)
        return sections_in_range

    def filter_by_course_number(self, request, sections):
        lower_course_number = request.get('num1')
        upper_course_number = request.get('num2')
        if upper_course_number and lower_course_number:
            return self.determine_courses_in_range(upper_course_number, lower_course_number, sections)
        elif lower_course_number:
            return sections.filter(Q(course__course_number=lower_course_number.upper()))
        return sections

    def filter_by_department(self, request, sections):
        department = request.get('dep')
        if department:
            return sections.filter(Q(course__department__abbr_name=department.upper()))
        return sections

    def filter_by_credits(self, request, sections):
        credit_hours = request.get('credits')
        if credit_hours:
            return sections.filter(Q(course__credit_hours=credit_hours))
        return sections

    def add_day_to_query(self, day_query, day):
        if day_query:
            day_query |= Q(meeting_times__day=day)
        else:
            day_query = Q(meeting_times__day=day)
        return day_query

    def filter_by_meeting_times(self, request, sections):
        start_time = request.get('stime')
        end_time = request.get('etime')
        day_query = Q()
        if request.get('mon'): day_query = self.add_day_to_query(day_query, 0)
        if request.get('tue'): day_query = self.add_day_to_query(day_query, 1)
        if request.get('wed'): day_query = self.add_day_to_query(day_query, 2)
        if request.get('thu'): day_query = self.add_day_to_query(day_query, 3)
        if request.get('fri'): day_query = self.add_day_to_query(day_query, 4)
        sections = sections.filter(day_query).distinct()
        if start_time and end_time:
            sections = sections.filter(Q(meeting_times__start_time__range=(start_time, end_time)))
            return sections.filter(Q(meeting_times__end_time__range=(start_time, end_time)))
        elif start_time:
            return sections.filter(Q(meeting_times__start_time=start_time))
        elif end_time:
            return sections.filter(Q(meeting_times__end_time=end_time))
        else:
            return sections

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['schedules'] = self.request.user.profile.schedule_set.all()
        return context

    def get_queryset(self):
        get_req = self.request.GET
        sections = Section.objects.all()
        sections = self.filter_by_professor(get_req, sections)
        sections = self.filter_by_name(get_req, sections)
        sections = self.filter_by_department(get_req, sections)
        sections = self.filter_by_credits(get_req, sections)
        sections = self.filter_by_meeting_times(get_req, sections)
        sections = self.filter_by_course_number(get_req, sections)
        return sections


@method_decorator(login_required, name='dispatch')
class ViewSectionView(View):
    template_name = 'student_assistance_system/view_section.html'

    def get(self, request, *args, **kwargs):
        section_id = self.kwargs['section_id']
        section = Section.objects.get(id=section_id)
        return render(request, self.template_name, dict(section=section))


@method_decorator(login_required, name='dispatch')
class ViewClass(View):

    def get(self, request, *args, **kwargs):
        p = request.user.profile
        return render(request, self.template_name, dict(user=p))


@method_decorator(login_required, name='dispatch')
class ViewScheduleView(IndexView):
    template_name = 'student_assistance_system/view_schedule.html'

    def get(self, request, *args, **kwargs):
        p = request.user.profile
        schedule = p.schedule_set.filter(pk=self.kwargs['schedule_id']).first()
        req_sets = self.get_requirement_sets(p)
        return render(request, self.template_name, dict(schedule=schedule, req_sets=req_sets, editing=self.kwargs['editing']))


@method_decorator(login_required, name='dispatch')
class RemoveSectionScheduleView(IndexView):
    template_name = 'student_assistance_system/view_schedule.html'

    def get(self, request, *args, **kwargs):
        p = request.user.profile
        schedule = p.schedule_set.filter(pk=self.kwargs['schedule_id']).first()
        req_sets = self.get_requirement_sets(p)
        section = schedule.sections.all().filter(pk=self.kwargs['section_id']).first()
        schedule.delete_section(section)
        return render(request, self.template_name, dict(schedule=schedule, req_sets=req_sets, editing=self.kwargs['editing']))

    def post(self, request, *args, **kwargs):
        p = request.user.profile
        schedule = self.request.POST.get('schedule')
        section = self.request.POST.get('section')
        schedule = p.schedule_set.get(id=schedule)
        section = Section.objects.get(id=section)
        schedule.delete_section(section)
        return HttpResponseRedirect(reverse('student_assistance_system:edit_schedule', args=(), kwargs={'schedule_id': schedule.id}))


@method_decorator(login_required, name='dispatch')
class AddSectionScheduleView(View):
    template_name = 'student_assistance_system/view_schedule.html'

    def post(self, request, *args, **kwargs):
        schedule = self.request.POST.get('schedule')
        section = self.request.POST.get('section')
        p = request.user.profile
        schedule = p.schedule_set.get(id=schedule)
        section = Section.objects.get(id=section)
        schedule.add_section(section)
        return HttpResponseRedirect(reverse('student_assistance_system:edit_schedule', args=(), kwargs={'schedule_id': schedule.id}))


@method_decorator(login_required, name='dispatch')
class ChangeNameScheduleView(View):
    template_name = 'student_assistance_system/view_schedule.html'

    def post(self, request, *args, **kwargs):
        schedule = self.request.POST.get('schedule')
        name = self.request.POST.get('name')
        p = request.user.profile
        schedule = p.schedule_set.get(id=schedule)
        schedule.change_name(name)
        return HttpResponseRedirect(reverse('student_assistance_system:edit_schedule', args=(), kwargs={'schedule_id': schedule.id}))


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'student_assistance_system/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def schedules_context_processor(request):
    u = request.user
    if u.is_anonymous():
        return dict()
    else:
        return dict(schedules=sorted(u.profile.schedule_set.all(), lambda x, y: -cmp(x.updated, y.updated)))
