from django import template

register = template.Library()


@register.inclusion_tag('student_assistance_system/fragments/schedule_view.html')
def schedule_view(schedule):
    return dict(schedule=schedule, editing=False)


@register.inclusion_tag('student_assistance_system/fragments/schedule_view.html')
def schedule_edit(schedule):
    return dict(schedule=schedule, editing=True)


@register.inclusion_tag('student_assistance_system/fragments/requirements_view.html', takes_context=True)
def requirements_view(context, req_sets):
    return dict(user=context['user'], req_sets=req_sets, schedule=context['schedule'])


@register.assignment_tag
def get_course_statuses(requirement, user, schedule):
    return requirement.get_course_statuses(user, schedule)


@register.assignment_tag
def fulfillment_status(requirement, course_statuses):
    return requirement.fulfillment_status(course_statuses)


@register.simple_tag
def long_status(abbr):
    if abbr == 'S':
        return "Fulfilled by schedule"
    elif abbr == 'U':
        return "Unfulfilled"
    else:
        return "Fulfilled"
