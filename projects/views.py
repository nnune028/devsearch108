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
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES) # FILES is necessary for image upload
        if form.is_valid():
            form.save() # Saves the data to the database
            return redirect('projects') # Takes the user back to the projects page

    context = {'form':form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login") # If not logged in, redirect to the login URL
def updateProject(request, pk):
    project = Project.objects.get(id=pk) # Gets the existing project
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
    project = Project.objects.get(id=pk) # Query object
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object':project}
    return render(request, "projects/delete_template.html", context)