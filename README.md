github comments tracker
=======================

assumes a settings.py file with the following content:

```
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
MONGO_DB = 'github_commenter'

# enter the relative path to your repo. example: github.com/davidbrai/github_comment_tracker -> davidbrai/github_comment_tracker
REPO_TO_FETCH = 'set your repo'
```

Running tests:
```
nosetests tests/
```

Running the server:
```
python app.py
```
