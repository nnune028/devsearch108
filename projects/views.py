from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects
from django.contrib import messages



# Create your views here.
def projects(request):
    projects, search_query = searchProjects(request)
    results = 3 # Number of results per page
    custom_range, projects = paginateProjects(request, projects, results)
    context = {'projects':projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)

    tags = projectObj.tags.all()
    context = {'project':projectObj, 'tags':tags, 'form':form}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login") # If not logged in, redirect to the login URL
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split() # Takes each word and splits by spaces

        form = ProjectForm(request.POST, request.FILES) # FILES is necessary for image upload
        if form.is_valid():
            project = form.save(commit=False) # Saves an instance of the project
            project.owner = profile
            project.save() # Saves the data to the database
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects') # Takes the user back to the projects page

    context = {'form':form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login") # If not logged in, redirect to the login URL
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project) # Form is assigned to the existing project

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split() # Takes each word and splits by spaces
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save() # Saves the data to the database
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects') # Takes the user back to the projects page

    context = {'form':form, 'project':project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login") # If not logged in, redirect to the login URL
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object':project}
    return render(request, "delete_template.html", context)