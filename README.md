github comments tracker
=======================

assumes a settings.py file with the following content:

```
GITHUB = {
	'consumer_key': '<github app client id>',
	'consumer_secret': '<github app client key>'
}

DEBUG = True

SECRET_KEY = 'development key'
MONGO_DB = 'github_commenter'
REPO_TO_FETCH = 'set your repo'
```

Running tests:
```
nosetests tests/
```
