from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django import forms
from .models import Team, Person, QuestionForm, FeedbackForm
from .trained_models.load_models import load_model

import pickle
import os
import numpy as np

# Load the William Hill latest trained model (the argument should be passed through the relevant config. Not harcoded.)
model = load_model('WIL')

# This is if the detectGuru part of the url is removed. Consider redirecting to a meaningful page.
def index(request):
    return HttpResponse("Hello, world. You're at the conference index.")


def detect_team_guru(request, project):
    team = get_object_or_404(Team, project_code=project)
    question_form = QuestionForm()
    feedback_form = FeedbackForm()
    context = {
        'team_name': team.name,
        'team_tag': team.project_code.lower(),
        'question_form': question_form,
        'feedback_form': feedback_form,
    }
    return render(request, 'conferenceLoader/question.html', context)

def team_people(request, project):
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
    question_form = QuestionForm(request.POST or None)
    if question_form.is_valid():
        question_form.save()
    context = {
        'results': detect_guru(request.POST.get("question")),
    }
    return render(request, 'conferenceLoader/results.html', context)




### Probably need to be moved elsewhere, to a util module
def detect_guru(text, n=-1):
    test = np.dstack([
        text
    ])
    test = np.array([t[0] for t in test])
    y = model.predict_proba(test)
    test_labels = model.classes_
    test_probs = y
    ordered = [[test_labels[i],test_probs[0][i],test_probs[0][i]] for i in range(test_labels.shape[0])]
    ordered.sort(key=lambda x: x[1],reverse=True)
    results = []
    for i in range(len(ordered)):
        if ordered[i][1]*100 >= 50:
            ordered[i][2] = "Absolute Guru"
        elif ordered[i][1]*100 >= 25:
            ordered[i][2] = "Guru"
        elif ordered[i][1]*100 >= 20:
            ordered[i][2] = "*****"
        elif ordered[i][1]*100 >= 15:
            ordered[i][2] = "****"
        elif ordered[i][1]*100 >= 10:
            ordered[i][2] = "***"
        elif ordered[i][1]*100 >= 4:
            ordered[i][2] = "**"
        elif ordered[i][1]*100 >= 2:
            ordered[i][2] = "*"
        else:
            ordered[i][2] = "Low probability compared to the rest"
        if (n<1 and int(ordered[i][1]*100) >= 1) or i < n:
            results.append([ordered[i][0],ordered[i][1],ordered[i][2]])
        else:
            break
        # results[ordered[i][0]] =  {
        #     'score': ordered[i][1],
        #     'assessment': ordered[i][2],
        # }
    return results