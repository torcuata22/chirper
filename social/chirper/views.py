from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'chirper/home.html', {})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'chirper/profile_list.html', {"profiles":profiles})

    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect ('home')



#10/24 stopped here: https://www.youtube.com/watch?v=fk8seSR148E&list=PLCC34OHNcOtoQCR6K4RgBWNi3-7yGgg7b&index=5
