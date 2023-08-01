''' This is a file for helper functions '''
from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page') # The page that displays in the results

    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page) # The page we want to get from the query set
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages # This directs us to the last page
        profiles = paginator.page(page)

    leftIndex = int(page) - 4

    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = int(page) + 2

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles


def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    skills = Skill.objects.filter(name__icontains=search_query) # iexact means it must match exactly, icontains can contain part of it
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | 
                                      Q(short_intro__icontains=search_query) |
                                      Q(skill__in=skills)) # The Q makes this an OR
    return profiles, search_query