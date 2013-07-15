#You need to create a new github application at this URL: https://github.com/settings/applications/new
#Then you should copy the keys from the app you created: "Client ID" to the consumer_key and "Client Secret" to the consumer_secret

GITHUB = {
    'consumer_key': '<github app client id>',
    'consumer_secret': '<github app client key>'
}

DEBUG = True

# could be any string you want. this is used by flask to encrypt stuff
SECRET_KEY = 'development key'

# choose whichever name you want for the mongodb name
MONGO_DB = 'github_comments'

# enter the relative path to your repo. example: github.com/davidbrai/github_comment_tracker -> davidbrai/github_comment_tracker
REPOS = ['repo1', 'repo2']

try:
    from local_config import *
except ImportError:
    # no local config found
    pass
