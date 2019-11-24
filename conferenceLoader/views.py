from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Team, Person
from .trained_models.load_models import load_model

import pickle
import os

# Consider moving elsewhere?
import numpy as np

# Load the William Hill latest trained model (the argument should be passed through the relevant config. Not harcoded.)
model = load_model('WIL')

# This is if the detectGuru part of the url is removed. Consider redirecting to a meaningful page.
def index(request):
    return HttpResponse("Hello, world. You're at the conference index.")


def detect_team_guru(request, project):
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


# The results page
def results(request, project):
    resp = "{0} - This is the Guru Results page.<br/>And the model classes:<br/>{1}</br>".format(project,model.classes_)
    resp2 = detect_guru('telebet migration offshore onshore')
    return HttpResponse(resp + resp2)




### Probably need to be moved elsewhere, to a util module
def detect_guru(text, n=10):
    resp = ""
    test = np.dstack([
        text
    ])
    test = np.array([t[0] for t in test])
    y = model.predict_proba(test)
    test_labels = model.classes_
    test_probs = y
    ordered = [[test_labels[i],test_probs[0][i],test_probs[0][i]] for i in range(test_labels.shape[0])]
    ordered.sort(key=lambda x: x[1],reverse=True)
    print("Top {0} results:".format(n))
    for i in range(n):
        if ordered[i][1]*100 > 40:
            ordered[i][2] = "Absolute Guru"
        elif ordered[i][1]*100 > 30:
            ordered[i][2] = "Guru"
        elif ordered[i][1]*100 > 20:
            ordered[i][2] = "*****"
        elif ordered[i][1]*100 > 10:
            ordered[i][2] = "****"
        elif ordered[i][1]*100 > 5:
            ordered[i][2] = "***"
        elif ordered[i][1]*100 > 2:
            ordered[i][2] = "**"
        elif ordered[i][1]*100 > 1:
            ordered[i][2] = "*"
        else:
            ordered[i][2] = "Not likely"
    resp += "num. &emsp; Name &emsp; Guru Meter <br>"
    for i in range(n):
        resp += "{0}. &emsp; {1} &emsp; {2} <br>".format(i+1, ordered[i][0], ordered[i][2])
    return resp