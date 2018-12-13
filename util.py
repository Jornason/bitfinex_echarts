import json
import urllib
import os
import io
import time
import datetime
import math
import string

from flask import Response


def json_response(status=200, obj={}, sort=True):
    # wrap a response
    r = {"_system": "geekree api system", "result": obj}
    return Response(
        response=json.dumps(r, ensure_ascii=False, sort_keys=sort, indent=2),
        status=200,
        mimetype="application/json")


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def url_decode(str):
    return urllib.parse.unquote(str)


