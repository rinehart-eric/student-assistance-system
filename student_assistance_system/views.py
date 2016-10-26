from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    schedules = request.user.profile.schedule_set.all()
    most_recently_updated_schedule = max(schedules, key=lambda s: s.updated) if schedules else None
    return render(request, 'student_assistance_system/index.html', dict(schedule=most_recently_updated_schedule))

@login_required
def view_schedule(request, schedule_id):
    schedule = request.user.profile.schedule_set.filter(pk=schedule_id).first()
    return render(request, 'student_assistance_system/view_schedule.html', dict(schedule=schedule))

@login_required
def profile(request):
    return render(request, 'student_assistance_system/profile.html', {
        'user': request.user,
    })
