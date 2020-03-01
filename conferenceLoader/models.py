from django.db import models
from django.forms import ModelForm, HiddenInput, RadioSelect, Textarea, CharField
from django.utils.timezone import now

# Team
# ----
# Represents a team in the company
# * name         - The full name of the team (eg. WIlliam Hill)
# * project_code - The abbreviated name of the team used in internal tools (eg. WIL)
class Team(models.Model):
    name = models.CharField(max_length=100)
    project_code = models.CharField(max_length=10)

    # The string representation of this object, should be its name
    def __str__(self):
        return self.name


# Stream
# ------
# Represents a stream (sub-team) inside a team.
# * name - The name of the stream
# * team - The team that it's part of
class Stream(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    # The string representation of this object, should be its name
    def __str__(self):
        return self.name



# Person
# ------
# Represents a person in the company
# * name     - The person's full name
# * username - The person's username (ldap)
# * role     - The person's role in the company (eg. Software Engineer L2)
# * team     - The team that the person currently belongs to
# * stream   - The stream of the team that the person currently belongs to
class Person(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    # The string representation of this object, should be its name
    def __str__(self):
        return self.name




# Conference
# ----------
# Represents an already trained model
# * file_name   - The name of the file that holds the saved model.
# * covering    - The internal team(s) that the model covers 
# * train_date  - The date that the model was trained
# * score       - The model's training score
# * source      - The source of information that was used to train the model (eg. JIRA)
# * description - Other information for the trained model
class Conference(models.Model):
    file_name = models.CharField(max_length=100)
    covering = models.CharField(max_length=100)
    train_date = models.DateTimeField('Date Trained')
    score = models.DecimalField(max_digits=19, decimal_places=3)
    source = models.CharField(max_length=100)
    description = models.CharField(max_length=400)

    # Change the string representation of this object to the date and score.
    def __str__(self):
        return self.train_date.strftime("%d/%m/%y") + " - Score: " + str(self.score)



# Default Team Conference
# -----------------------
# Represents the default trained model selected for a Team that will be generating predictions.
# * team  - The team for which this particular model is the default.
# * model - The model that is the the default for the team.
class DefaultTeamConference(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    model = models.ForeignKey(Conference, on_delete=models.CASCADE)

    # Change the string representation of this object to the date and score.
    def __str__(self):
        return str(self.team) + " -- " + str(self.model)



# Question
# -------
# Represents the question that is being asked from someone in order to detect gurus about it.
# * question - The question itself as was input by the user
# * datetime - Date and time that the question was asked
class Question(models.Model):
    question = models.CharField(max_length=500, default='')
    datetime = models.DateTimeField('Date asked', default=now)

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'datetime']
        labels = {'question': ''}
        widgets = {'datetime': HiddenInput(),}



# Feedback
# --------
# Represents the feedback we wish to get from the users
# * question     - The question that was asked (foreign key)
# * feedback_det - Detailed feedback in plain text by the user, if given.
class Feedback(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    datetime = models.DateTimeField('Date submitted', default=now)
    name = models.CharField(max_length=20, blank=True, default='')
    feedback_det = models.CharField(max_length=2000)

    def __str__(self):
        if self.name == '':
            return str("Anonymous - " + str(self.datetime))
        else:
            return str(self.name) + " - " + str(self.datetime)

class FeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['feedback_det'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Feedback
        fields = ['name','feedback_det','datetime']
        labels = {
            'name': 'Name (optional):',
            'feedback_det': 'Feedback:',
        }
        widgets = {
            # 'question': HiddenInput(),
            # 'datetime': HiddenInput(),
            'feedback_det':Textarea(attrs={'rows':5,}),
        }

