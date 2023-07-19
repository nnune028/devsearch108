from django.db import models
import uuid

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)
    # Allowed to create a record without a description, null for db, blank for Django
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # Automatically generates a timestamp
    created = models.DateTimeField(auto_now_add=True)
    # Unique, primary key of the table, and not editable
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): # This is what allows us to see the project by its title name in the db in the admin panel
        return self.title
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # owner =
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # Delete all reviews if project deleted
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    # Automatically generates a timestamp
    created = models.DateTimeField(auto_now_add=True)
    # Unique, primary key of the table, and not editable
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): # This is what allows us to see the project by its title name in the db in the admin panel
        return self.value
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    # Automatically generates a timestamp
    created = models.DateTimeField(auto_now_add=True)
    # Unique, primary key of the table, and not editable
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self): # This is what allows us to see the project by its title name in the db in the admin panel
        return self.name