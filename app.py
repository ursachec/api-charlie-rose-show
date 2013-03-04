import os
import json
from app.db.charlierosedb import CharlieRoseDatabaseManager
from app.config.db import DB_CONFIG, VIDEO_SOURCE_URL, IMAGE_SOURCE_URL

from functools import wraps
from flask import Flask, make_response, redirect
app = Flask(__name__)
dbManager = CharlieRoseDatabaseManager()

def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator

def contenttypejson(f):
    """This decorator passes Content-Type: application/json"""
    @wraps(f)
    @add_response_headers({'Content-Type': 'application/json'})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def noindex(f):
    """This decorator passes X-Robots-Tag: noindex"""
    @wraps(f)
    @add_response_headers({'X-Robots-Tag': 'noindex'})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@noindex
def hello():
    return "{hello from the charlie rose api}"

@app.route('/shows/<show_id>')
@contenttypejson
@noindex
def show_post(show_id):
    someShows = dbManager.fetchSingleShowForIdString(show_id)
    return json.dumps(someShows)

@app.route('/shows/topic/<topic_id>')
@contenttypejson
@noindex
def shows_for_topic(topic_id):
    print "shows_for_topic"
    someShows = []
    someShows = dbManager.fetchShowsForTopicString(topic_id)
    return json.dumps(someShows)

@app.route('/videos/<show_id>')
@contenttypejson
@noindex
def show_video(show_id):
    url = '{0}{1}'.format(VIDEO_SOURCE_URL, str(show_id))
    return redirect(url, 301)

@app.route('/images/<show_id>')
@contenttypejson
@noindex
def show_image(show_id):
    url = '{0}{1}.png'.format(IMAGE_SOURCE_URL, str(show_id))
    return redirect(url, 301)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
