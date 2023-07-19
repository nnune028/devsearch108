from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag # Must import this to add it to the admin panel

admin.site.register(Project) # Must add this to add it to the admin panel
admin.site.register(Review) # Must add this to add it to the admin panel
admin.site.register(Tag) # Must add this to add it to the admin panel