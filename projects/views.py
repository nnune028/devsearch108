from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def projects(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    context = {'project':projectObj, 'tags':tags}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login") # If not logged in, redirect to the login URL
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES) # FILES is necessary for image upload
        if form.is_valid():
            project = form.save(commit=False) # Saves an instance of the project
            project.owner = profile
            project.save() # Saves the data to the database
            return redirect('projects') # Takes the user back to the projects page

    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login") # If not logged in, redirect to the login URL
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project) # Form is assigned to the existing project

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save() # Saves the data to the database
            return redirect('projects') # Takes the user back to the projects page

    context = {'form':form}
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