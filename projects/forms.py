from django.forms import ModelForm
from django import forms # Allows us to modify fields
from .models import Project

class ProjectForm(ModelForm):
    class Meta: # Metadata attached to the model
        model = Project
        # fields = '__all__' # Takes everything that is editable in the model
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs) # Inherit from the ProjectForm class

        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add title'}) # Update the class and make it an input field
        # self.fields['description'].widget.attrs.update({'class':'input', 'placeholder':'Description here'})

        # Iterates throught the dictionary instead of doing each one individually
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input', 'placeholder':'Insert ' + name + ' here'})