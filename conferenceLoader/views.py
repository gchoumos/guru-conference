from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django import forms
from gensim.parsing.preprocessing import STOPWORDS
from .models import Team, Person, QuestionForm, FeedbackForm
from .trained_models.load_models import load_model

import pickle
import os
import re
import string
import numpy as np

# Load the William Hill latest trained model (the argument should be passed through the relevant config. Not harcoded.)
model = load_model('WIL')

# Stop words - This should be read from the settings that the preprocessor also uses. This is Technical Debt!
# These are in addition to the stopwords.
# h1-h6: Jira comment notation for headers
# p1-p5: The Jira priorities
WORDS_TO_IGNORE = {
  '2char': [
    'll',
    'hi',
    'cc',
    'wh',
    'im',
    'p1', 'p2', 'p3', 'p4', 'p5',
    '1g', '2g', '3g', '4g', '5g', '6g', '7g', '8g',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'kb',
  ]
}
stopwords = set(STOPWORDS)
for x in WORDS_TO_IGNORE['2char']:
    stopwords.add(x)


# This is if the detectGuru part of the url is removed. Consider redirecting to a meaningful page.
def index(request):
    return HttpResponse("Hello world. You're at the conference index.")


def detect_team_guru(request, project):
    team = get_object_or_404(Team, project_code=project)
    question_form = QuestionForm()
    feedback_form = FeedbackForm(request.POST or None)
    feedback_form.datetime = timezone.localtime()
    if feedback_form.is_valid():
        feedback_form.save()
        return HttpResponseRedirect(request.path_info)
    context = {
        'team_name': team.name,
        'team_tag': team.project_code.lower(),
        'question_form': question_form,
        'feedback_form': feedback_form,
        'project': project,
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
    feedback_form = FeedbackForm(request.POST or None)
    feedback_form.datetime = timezone.localtime()
    if feedback_form.is_valid():
        feedback_form.save()
        return HttpResponseRedirect(request.path_info)
    if question_form.is_valid():
        question_form.save()
    question = request.POST.get("question")
    # preprocess user query
    question = preprocess(question)
    results = detect_guru(question)
    results_context = []
    for i in results:
        person = Person.objects.get(username=i[0])
        results_context.append(
            i + [
                    person.name,
                    person.role,
                    person.team,
                    person.stream,
                    person.location,
                    person.slack_id,
                ]
        )
    # results[i][0]: username
    # results[i][1]: guru percentage
    # results[i][2]: guru level stars
    # results[i][3]: guru level comment
    # results[i][4]: guru badge class (bootstrap)
    # results[i][5]: full name
    # results[i][6]: role
    # results[i][7]: team
    # results[i][8]: stream
    # results[i][9]: location
    # results[i][10]: slack ID
    print("Results context: {0}".format(results_context))
    context = {
        'results': results_context,
        'question': question,
        'feedback_form': feedback_form,
        'project': project,
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
    ordered = [[test_labels[i],test_probs[0][i],test_probs[0][i],'',''] for i in range(test_labels.shape[0])]
    ordered.sort(key=lambda x: x[1],reverse=True)
    results = []
    for i in range(len(ordered)):
        if ordered[i][1]*100 >= 35:
            ordered[i][2] = "*******"
            ordered[i][3] = "Guru"
            ordered[i][4] = "dark"
        elif ordered[i][1]*100 >= 25:
            ordered[i][2] = "******"
            ordered[i][3] = "Master"
            ordered[i][4] = "danger"
        elif ordered[i][1]*100 >= 20:
            ordered[i][2] = "*****"
            ordered[i][3] = "Expert"
            ordered[i][4] = "warning"
        elif ordered[i][1]*100 >= 15:
            ordered[i][2] = "****"
            ordered[i][3] = "Proficient"
            ordered[i][4] = "primary"
        elif ordered[i][1]*100 >= 10:
            ordered[i][2] = "***"
            ordered[i][3] = "Competent"
            ordered[i][4] = "info"
        elif ordered[i][1]*100 >= 4:
            ordered[i][2] = "**"
            ordered[i][3] = "Advanced Beginner"
            ordered[i][4] = "secondary"
        elif ordered[i][1]*100 >= 2:
            ordered[i][2] = "*"
            ordered[i][3] = "Novice"
            ordered[i][4] = "success"
        else:
            ordered[i][2] = "Low probability compared to the rest"
        if (n<1 and int(ordered[i][1]*100) >= 2) or i < n:
            results.append([ordered[i][0],ordered[i][1],ordered[i][2],ordered[i][3],ordered[i][4]])
        else:
            break
    return results


def preprocess(question):
    # **NOT** cleaning newlines and carriage returns
    # --
    # Remove URLs - possibly unneeded
    print("Initial question: {0}".format(question))
    question = re.sub(r'((https?:\/\/)|(www\.))[^\s]*','',question)
    print("Removed URLs: {0}".format(question))
    # Remove e-mails - possibly unneeded
    question = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+','',question)
    print("Removed e-mails: {0}".format(question))
    # Remove multiple spaces
    question = re.sub(r'\s+',' ',question)
    print("Removed multiple spaces: {0}".format(question))
    # **NOT** fixing bad tag cases
    # --
    # Removing special tags - possibly unneeded
    question = re.sub('r(\{[Cc]olor.*?\}(.*?)\{[Cc]olor\})','',question)
    print("Removed special tags: {0}".format(question))
    # **NOT** extracting code/quotes/noformats/panels
    # --
    # Removing punctuation apart from dashes (-) and underscores(_)
    punct = '|'.join([re.escape(x) for x in string.punctuation.replace('-','').replace('_','')])
    question = re.sub(punct,' ',question)
    print("Removed punctuation: {0}".format(question))
    # Remove multiple spaces again
    question = re.sub(r'\s+',' ',question)
    print("Removed multiple spaces again: {0}".format(question))
    # Remove digit-only words (the following 2 lines can become one)
    question = ' '.join([word for word in question.split() if not word.isdigit()])
    print("Removed digit-only words: {0}".format(question))
    # Remove small words - (minimum length is 2)
    minlen = 2
    question = ' '.join([word for word in question.split() if len(word) >= minlen])
    print("Removed small words: {0}".format(question))
    # Convert to lowercase
    question = question.lower()
    print("Convert to lowercase: {0}".format(question))
    # Now stopwords...
    question = ' '.join([word for word in question.split() if word not in stopwords])
    # Remove punctuation-only words
    question = ' '.join([word for word in question.split() if not all(c in string.punctuation for c in word)])
    print("Removing stopwords: {0}".format(question))
    return question
