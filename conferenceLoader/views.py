from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Team, Person

# This is if the detectGuru part of the url is removed. Consider redirecting to a meaningful page.
def index(request):
    return HttpResponse("Hello, world. You're at the conference index.")


def detect_guru(request, project):
    team = get_object_or_404(Team, project_code=project)
    context = {
        'team_name': team.name,
        'team_people': Person.objects.all().filter(team=team.pk),
    }
    return render(request, 'conferenceLoader/team_people.html', context)


# This is the case where a team has not been specified. Later on it should be updated so that
# the user will have the ability to change a Team from a list.
def detect_guru_no_spec(request):
    return HttpResponse("A Team has not been specified. Did you manually modify the URL?")


# The response page
def results(request, project):
    return HttpResponse("{0} - This is the Guru Results page.".format(project))
