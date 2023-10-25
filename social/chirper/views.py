from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Profile, Chirp
from .forms import ChirpForm, SignUpForm

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

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) #calls djangon authentication system
     
        if user is not None:
            login(request, user)
            messages.success(request, ("Login successful!"))
            return redirect('home')
        else:
            messages.success(request, ("Oops, something went wrong. Please try again"))
            return redirect('login')


    else:    
        return render(request, 'chirper/login.html', {})



def logout_user(request):
    logout(request)
    messages.success(request, ("You have logged out successfully"))
    return redirect('login')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# first_name = form.cleaned_data['first_name']
			# second_name = form.cleaned_data['second_name']
			# email = form.cleaned_data['email']
			# Log in user
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ("You have successfully registered! Welcome!"))
			return redirect('home')
	
	return render(request, "chirper/register.html", {'form':form})              



#10/25 stopped here: