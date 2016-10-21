from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    return render(request, 'student_assistance_system/index.html')

@login_required
def profile(request):
    return render(request, 'student_assistance_system/profile.html', {
        'user': request.user,
    })
