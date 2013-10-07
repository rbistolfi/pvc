# coding: utf-8


from eve import Eve
from flask import Flask, render_template
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple


backend = Eve()
frontend = Flask(__name__)


@frontend.route("/")
def index():
    return render_template("index.html")


app = DispatcherMiddleware(backend, {"/p": frontend})


if __name__ == "__main__":

    import os

    host = os.environ.get("host")
    port = int(os.environ.get("port"))
    run_simple(host, port, app, use_reloader=True)
