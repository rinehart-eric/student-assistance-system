from django import template

register = template.Library()


@register.inclusion_tag('student_assistance_system/fragments/schedule_view.html')
def schedule_view(schedule):
    return dict(schedule=schedule)


@register.inclusion_tag('student_assistance_system/fragments/requirements_view.html')
def requirements_view(req_sets):
    return dict(req_sets=req_sets)
