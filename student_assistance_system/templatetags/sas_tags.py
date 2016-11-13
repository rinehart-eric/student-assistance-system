from django import template

register = template.Library()


@register.inclusion_tag('student_assistance_system/fragments/schedule_view.html')
def schedule_view(schedule):
    return dict(schedule=schedule)


@register.inclusion_tag('student_assistance_system/fragments/requirements_view.html', takes_context=True)
def requirements_view(context, req_sets):
    return dict(user=context['user'], req_sets=req_sets)


@register.simple_tag
def fulfilled(requirement, user):
    return requirement.is_fulfilled_by(user)
