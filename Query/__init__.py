"""
Azure Function
Same functionality, now cheap (or free) for low volume usage
"""

import logging
import runpy
from .reddit_user import RedditUser, UserNotFoundError, NoDataError
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get('username')

    if name:
        try:
            runpy.run_module('textblob.download_corpora', run_name='__main__')
            u = RedditUser(name, complete_query=False)
            return func.HttpResponse(str(u.results()))
        except UserNotFoundError:
            return func.HttpResponse(
                '{"_errors":[{"User %s not found"}]}' % name)
        except NoDataError:
            return func.HttpResponse(
                '{"_errors":[{"No data available for user %s"}]}' % name)
    else:
        return func.HttpResponse(
             '{"_errors":[{"User %s not found"}]}' % name)
