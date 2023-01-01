from flask import g, Flask, request, send_file, redirect, session, jsonify
from flask import render_template as render_template_default
import os
import re
from werkzeug.utils import secure_filename

from flask import Response
from jinja2 import Template, FunctionLoader, Environment, BaseLoader
from flask import Flask
import mimetypes
import datetime
from peewee import *
from database import *
from playhouse.shortcuts import model_to_dict
import zipfile
from flask_caching import Cache
from baselib import *
from request_vars import *

# NOTE: Константы
UPLOAD_PATH_REL = "static/uploads"
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), UPLOAD_PATH_REL)

# NOTE: Переменные, Приложение flask(app)
print("[!] INIT APP DATABASE=", DATABASE, " bFirstStart=", bFirstStart)
app = Flask(__name__)
config = {
    # "DEBUG": True,          # some Flask specific configs
    # "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)

@app.route("/zip/static/<path:path>", methods=['GET', 'POST'])
def zip_static(path):
    oR = Response(readfile("static/"+path), mimetype=mimetypes.guess_type(path)[0])
    oR.headers['Cache-Control'] = 'max-age=60480000, stale-if-error=8640000, must-revalidate'
    return oR

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return 's'+''.join(x.title() for x in components[0:])

def fnPrepareArgs(oR):
    oR.oArgs = parse_get(request.args)
    oR.oArgsLists = parse_multi_form(request.args)

    for sK in oR.oArgs:
        sVarName = to_camel_case(sK)
        setattr(oR, sVarName, oR.oArgs[sK])

def fnPrepareProjectsData(oR):
    oR.sBaseURL = request.url

    fnPrepareArgs(oR)

    oR.oProjects = Project.select()
    oR.oGroups = Group.select().where(Group.project==oR.sSelectProject)
    # print(oR.oGroups[0].name)
    oR.lTasks = []
    for oGroup in oR.oGroups:
        oR.lTasks.append(Task.select().where(Task.group==oGroup.id))

@app.route("/", methods=['GET', 'POST'])
@cache.cached()
def index():
    oIndex = Notes.get(Notes.name=='index')
    return render_template(
        'index.html', 
        oIndex=oIndex
    )

@app.route("/projects/kanban", methods=['GET', 'POST'])
@cache.cached()
def projects_kanban():
    oR = RequestVars()
    fnPrepareProjectsData(oR)

    return render_template(
        'projects_kanban.html', 
        oR=oR
    )

@app.route("/projects/list", methods=['GET', 'POST'])
@cache.cached()
def projects_list():
    oR = RequestVars()
    fnPrepareProjectsData(oR)

    return render_template(
        'projects_list.html', 
        oR=oR
    )

@app.route("/metrics", methods=['GET', 'POST'])
@cache.cached()
def metrics():
    return render_template(
        'metrics.html', 
    )

@app.route("/files", methods=['GET', 'POST'])
@cache.cached()
def files():
    return render_template(
        'files.html', 
    )

@app.route("/notes", methods=['GET', 'POST'])
@cache.cached()
def notes():
    return render_template(
        'notes.html', 
    )

def run():
    print("[!] RUN ON HOST 0.0.0.0")
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    run()