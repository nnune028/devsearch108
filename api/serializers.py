from rest_framework import serializers
from projects.models import Project

class ProjectSerializer(serializers.ModelSerializer): # Converts Project fields into JSON objects
    class Meta:
        model = Project
        fields = '__all__'