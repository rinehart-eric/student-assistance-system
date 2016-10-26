from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    schedules = request.user.profile.schedule_set.all()
    most_recently_updated_schedule = max(schedules, key=lambda s: s.updated)
    return render(request, 'student_assistance_system/index.html', dict(schedule=most_recently_updated_schedule))

@login_required
def profile(request):
    return render(request, 'student_assistance_system/profile.html', {
        'user': request.user,
    })
