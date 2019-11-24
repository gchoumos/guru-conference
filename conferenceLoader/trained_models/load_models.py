import pickle
import os

# Add a comment later
def load_model(project="WIL"):
    MODEL_PATH = '/home/gchoumo/Dropbox/Code/jira-guru-detector/guruDetector/'
    MODEL_NAME = 'latest_model'

    # Load the model
    return pickle.load(open(os.path.join(MODEL_PATH,MODEL_NAME),'rb'))