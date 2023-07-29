from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

''' Renders the login page '''
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist!')

        user = authenticate(request, username=username, password=password) # Queries database and returns the username and password if there
        
        if user is not None:
            login(request, user) # Creates session for user in database, adds session to the browser's cookies
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect.')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request) # Deletes the session
    messages.success(request, 'User was successfully logged out.')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Holding a temporary instance of the user (in case we want to modify)
            user.username = user.username.lower() # To prevent case sensitivity
            user.save() # Now added to the database and saved

            messages.success(request, 'User successfully created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occurred during registration.')

    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):

    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description="") # This excludes the skills that don't have a description
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all() # This excludes the skills that don't have a description
    projects = profile.project_set.all()

    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)