from flask import Flask, session, redirect, url_for, jsonify
from flask_oauthlib.client import OAuth
import logging
logging.basicConfig(level=logging.INFO)

from github import Github

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('settings')

oauth = OAuth(app)
github_app_settings = app.config['GITHUB']
github = oauth.remote_app(
    'github',
    consumer_key=github_app_settings['consumer_key'],
    consumer_secret=github_app_settings['consumer_secret'],
    request_token_params={'scope': 'repo'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@app.route("/")
def index():
    if not 'github_token' in session:
        log.info("redirecting to login")
        return redirect(url_for('login'))

    log.info("getting comments from github")
    github_client = Github(session['github_token'][0])
    repo = github_client.get_repo(app.config['REPO_TO_FETCH'])
    comments_text = []
    comments = repo.get_comments()
    for i, comment in enumerate(comments[:20]):
        log.info("at comment: %s" % i)
        comments_text.append(comment.body)
    log.info("got: %s", comments_text[:5])
    return jsonify({'comments': comments_text})

@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
@github.authorized_handler
def authorized(resp):
    log.info("authorized!")

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['github_token'] = (resp['access_token'], '')
    return redirect(url_for('index'))

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

if __name__ == "__main__":
    app.run()
