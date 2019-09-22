from django.db import models

# Team
# ----
# Represents a team in the company
# * name         - The full name of the team (eg. WIlliam Hill)
# * project_code - The abbreviated name of the team used in internal tools (eg. WIL)
class Team(models.Model):
    name = models.CharField(max_length=100)
    project_code = models.CharField(max_length=10)



# Stream
# ------
# Represents a stream (sub-team) inside a team.
# * name - The name of the stream
# * team - The team that it's part of
class Stream(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)



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



# Question
# -------
# Represents the question that is being asked from someone in order to detect gurus about it.
# * text - The question itself as was input by the user
# * date - Date that the question was asked
class Question(models.Model):
    text = models.CharField(max_length=1000)
    date = models.DateTimeField('Date asked')



# Feedback
# --------
# Represents the feedback we wish to get from the users
# * question     - The question that was asked (foreign key)
# * feedback_gen - A general, high-level feedback in terms of useful/not-useful
# * feedback_det - Detailed feedback in plain text by the user, if given.
class Feedback(models.Model):
    USEFUL = 'Y'
    NOT_USEFUL = 'N'
    NO_RESPONSE = '-'
    FEEDBACK_CHOICES = [
        (USEFUL, 'Useful'),
        (NOT_USEFUL, 'Not useful'),
        (NO_RESPONSE, 'Provide no feedback'),
    ]
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    feedback_gen = models.CharField(max_length=1,choices=FEEDBACK_CHOICES,default=NO_RESPONSE)
    feedback_det = models.CharField(max_length=2000)


