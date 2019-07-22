"""
Flask application / Azure webapp entry point added by SockHungryClutz
"""

from flask import Flask, request
from reddit_user import RedditUser, UserNotFoundError, NoDataError
import logging
from logging.handlers import RotatingFileHandler
app = Flask(__name__)

@app.route("/query")
def query():
    user = request.args.get('username', default="_", type=str)
    try:
        u = RedditUser(user, complete_query=False)
        return str(u.results())
    except UserNotFoundError:
        return '{"_errors":[{"User %s not found"}]}' % user
    except NoDataError:
        return '{"_errors":[{"No data available for user %s"}]}' % user

@app.route("/fullquery")
def fullquery():
    user = request.args.get('username', default="_", type=str)
    try:
        u = RedditUser(user)
        return str(u.results())
    except UserNotFoundError:
        return '{"_errors":[{"User %s not found"}]}' % user
    except NoDataError:
        return '{"_errors":[{"No data available for user %s"}]}' % user

if __name__ == '__main__':
    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()