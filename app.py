import json
from flask import Flask, session, redirect, url_for, request, render_template
from flask_oauthlib.client import OAuth
import dao
import logging
import datetime
from flask.wrappers import Response
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

def fetch_comments_from_github(repo, max_comments=None):
    comments = repo.get_comments()
    for i, c in enumerate(comments[:max_comments]):
        log.info("At comment %d" % i)
        comment = {
            'id': c.id,
            'body': c.body,
            'url': c.html_url,
            'user_id': c.user.id,
            'user_login': c.user.login,
            'commit': c.commit_id,
            'line': c.line,
            'path': c.path,
            'created_at': c.created_at,
            'avatar_url': c.user.avatar_url
        }
        dao.save_to_thread(comment)

def datetime_json_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat() 

@app.route("/fetch_comments/<int:max_comments>")
def login_to_github_and_get_all_comments(max_comments):
    if not is_logged_in():
        log.info("redirecting to login")
        return redirect(url_for('login'))

    log.info("getting comments from github")
    github_client = Github(session['github_token'][0], per_page=100)
    repo = github_client.get_repo(app.config['REPO_TO_FETCH'])
    fetch_comments_from_github(repo, max_comments)
    return redirect(url_for('comments'))

@app.route("/fetch_comments")
def fetch_comments():
    return login_to_github_and_get_all_comments(max_comments=None)

def jsonify(data):
    return Response(json.dumps(data, default=datetime_json_handler, indent=2), mimetype='application/json')

@app.route("/")
def comments():
    if not is_logged_in():
        log.info("redirecting to login")
        return redirect(url_for('login'))

    return render_template('comments.html')

@app.route("/threads")
def my_threads():
    return jsonify(dao.get_user_threads(session['github_user_id']))

@app.route("/threads/all")
def all_threads():
    return jsonify(dao.get_all_threads())

@app.route("/thread/<thread_id>/mark_as_read", methods=['POST'])
def mark_thread_as_read(thread_id):
    dao.mark_thread_as_read(session['github_user_id'], thread_id)
    return ''

@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('github_user_id', None)
    session.pop('github_token', None)
    return redirect(url_for('comments'))

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
    session['github_user_id'] = github.get('user').data['id']
    return redirect(url_for('comments'))

@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

def is_logged_in():
    return 'github_token' in session

if __name__ == "__main__":
    app.run()
