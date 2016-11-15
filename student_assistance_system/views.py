from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View, generic
from .models import Section


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    template_name = 'student_assistance_system/index.html'

    def get_requirement_sets(self, p):
        majors_and_concentrations = [(um.major, um.concentration) for um in p.usermajor_set.all()]
        return list(p.minors.all()) + list(sum(majors_and_concentrations, ()))

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
    template_name = 'student_assistance_system/search_results.html'
    context_object_name = "sections"
    paginate_by = 1

    def get_queryset(self):
        get_req = self.request.GET
        name = get_req.get('name')
        lower_course_number = get_req.get('num1')
        upper_course_number = get_req.get('num2')
        department = get_req.get('dep')
        professor = get_req.get('prof')
        sections = Section.objects.all()
        if professor:
            sections.filter(professor=professor)
        print(sections)
        return sections

@method_decorator(login_required, name='dispatch')
class ViewScheduleView(IndexView):
    template_name = 'student_assistance_system/view_schedule.html'

    def get(self, request, *args, **kwargs):
        p = request.user.profile
        schedule = p.schedule_set.filter(pk=self.kwargs['schedule_id']).first()
        req_sets = self.get_requirement_sets(p)

        return render(request, self.template_name, dict(schedule=schedule, req_sets=req_sets))


@method_decorator(login_required, name='dispatch')
class EditScheduleView(View):
    template_name = 'student_assistance_system/edit_schedule.html'

    def get(self, request, *args, **kwargs):
        p = request.user.profile
        schedule = p.schedule_set.filter(pk=self.kwargs['schedule_id']).first()

        # TODO: create this template
        return render(request, self.template_name, dict(schedule=schedule))


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'student_assistance_system/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, dict(user=request.user))
