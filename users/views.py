from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles

# Create your views here.

''' Renders the login page '''
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist!')

        user = authenticate(request, username=username, password=password) # Queries database and returns the username and password if there
        
        if user is not None:
            login(request, user) # Creates session for user in database, adds session to the browser's cookies
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
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
            return redirect('profile')
        else:
            messages.error(request, 'An error has occurred during registration.')

    context = {'page':page, 'form':form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)

    results = 1
    custom_range, profiles = paginateProfiles(request, profiles, results)


    context = {'profiles':profiles, 'search_query':search_query, 'custom_range':custom_range}
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


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('account')

    context = {'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    context = {'object':skill}
    return render(request, 'delete_template.html', context)