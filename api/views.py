from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},
        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
# @permission_classes([IsAuthenticated]) # Now the user must be authenticated if they want to get projects
def getProjects(request):
    print(f'USER: {request.user}')
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True) # We are serializing many objects, not just one
    return Response(serializer.data) # This gives us the serialized projects

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False) # We are serializing many objects, not just one
    return Response(serializer.data) # This gives us the serialized projects