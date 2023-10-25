from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Chirp
from .forms import ChirpForm

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = ChirpForm(request.POST or None)
        if request.method == 'POST':

            if form.is_valid():
                chirp = form.save(commit=False)
                chirp.user = request.user
                chirp.save()
                messages.success(request, ("Your chirp has been heard!"))
                return redirect('home')

        chirps = Chirp.objects.all().order_by("-created_at")
        return render(request, 'chirper/home.html', {'chirps':chirps, 'form':form})
    else:
        chirps = Chirp.objects.all().order_by("-created_at")
        return render(request, 'chirper/home.html', {'chirps':chirps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'chirper/profile_list.html', {"profiles":profiles})

    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect ('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        chirps = Chirp.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
                current_user_profile.save()

        return render(request, 'chirper/profile.html', {'profile' : profile, 'chirps':chirps})

    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect ('home')








#10/25 stopped here: