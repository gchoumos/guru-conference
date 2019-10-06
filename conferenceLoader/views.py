from django.shortcuts import render
from django.http import HttpResponse
from .models import Team
from .models import Person

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the conference index.")

def detect_guru(request, project):
    try:
        team_name = Team.objects.get(project_code=project).name
        team_pk = Team.objects.get(project_code=project).pk
        team_people = Person.objects.all().filter(team=team_pk)
        output = "Guru Detector for {0}.\n".format(team_name)
        output += "Here are the people of the team:\n"
        output += '\n'.join(x.name for x in team_people)
        return HttpResponse(output)
        # return HttpResponse("Guru Detector for {0}".format(team_name))
    except Team.DoesNotExist:
        return HttpResponse("The team corresponding to {0} does not exist. Did you manually modify the URL?".format(project))

# This is the case where a team has not been specified. Later on it should be updated so that
# the user will have the ability to change a Team from a list.
def detect_guru_no_spec(request):
    return HttpResponse("A Team has not been specified. Did you manually modify the URL?")