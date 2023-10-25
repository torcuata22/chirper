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


def profile(request, pk):
    #make sure user is logged in:
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        return render(request, 'chirper/profile.html', {'profile' : profile})

    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect ('home')








#10/25 stopped here: