from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile, Chirp
from .forms import ChirpForm, SignUpForm, UpdateUserForm, ProfilePicForm

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
    

@login_required
def update_user(request):
     if request.user.is_authenticated:
          current_user = User.objects.get(id=request.user.id)
          profile_user = Profile.objects.get(user__id = request.user.id)
          #get forms:
          user_form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)
          profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance = profile_user)
          if user_form.is_valid() and profile_form.is_valid():
               user_form.save()
               profile_form.save()
               login(request, current_user)
               messages.success(request, ("Your profile has been updated"))
               return redirect('home')

          return render(request, 'chirper/update_user.html', {'user_form':user_form, 'profile_form':profile_form})
     else:
          messages.success(request,("You must be signed in to see this page"))
          return redirect('home')    

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

def chirp_like(request, pk):
    if request.user.is_authenticated:
        chirp = get_object_or_404(Chirp, id=pk)
        if chirp.likes.filter(id=request.user.id):
            chirp.likes.remove(request.user)
        else:
            chirp.likes.add(request.user)
    else:
        messages.success(request, ("You must be logged in to like a Chirp"))
    
    return redirect (request.META.get('HTTP_REFERER'))

def chirp_show(request, pk):
    chirp = get_object_or_404(Chirp, id=pk)
    if chirp:
        return render(request, 'chirper/show.html', {'chirp':chirp})

    else:
        messages.success(request, ("That Chirp doesn't exist"))
        return redirect('home')
    



#TODO: Research: How to add pop up box to add your comments and share a “chirp”    
        

#AUTHENTICATION VIEWS

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