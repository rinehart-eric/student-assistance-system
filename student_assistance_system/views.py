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

    def filter_by_course_number(self, request, sections):
        lower_course_number = request.get('num1')
        upper_course_number = request.get('num2')
        if lower_course_number:
            return sections.filter(Q(course__course_number=lower_course_number))
        return sections

    def filter_by_department(self, request, sections):
        department = request.get('dep')
        if department:
            return sections.filter(Q(course__department__abbr_name=department.upper()))
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
