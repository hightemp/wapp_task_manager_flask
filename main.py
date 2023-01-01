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

def fnPrepareFormArgs(oR, sName):
    oR.oArgs = parse_get(request.args)
    oR.oArgsLists = parse_multi_form(request.args)

    for sK in oR.oArgs:
        # sVarName = to_camel_case(sK)
        sVarName = ""
        setattr(oR, sVarName, oR.oArgs[sK])

def fnPrepareProjectsData(oR):
    oR.sBaseURL = request.url

    fnPrepareArgs(oR)

    oR.oProjects = Project.select().where(Project.name ** f"%{oR.sSearchProject}%").order_by(-Project.sort)
    oR.oGroups = Group.select().where(Group.project==oR.sSelectProject).order_by(+Group.sort)

    if "select-task" in oR.oArgs:
        oR.oTask = Task.get_by_id(oR.sSelectTask)
        oR.oTaskComments = Comment.select().where(Comment.task==oR.sSelectTask).order_by(-Comment.id)
        oR.oTaskFiles = File.select().where(File.task==oR.sSelectTask)
    if "create-project" in oR.oArgs:
        oR.dProjectFieldsV = fnPrepareFormFields(oR.dProjectFields, Project, 0)
    if "edit-project" in oR.oArgs:
        oR.dProjectFieldsV = fnPrepareFormFields(oR.dProjectFields, Project, oR.sEditProject)
    if "create-group" in oR.oArgs:
        oR.dGroupFields['project']['list'] = Project.select()
        oR.dGroupFields['project']['sel_value'] = oR.sSelectProject
        oR.dGroupFieldsV = fnPrepareFormFields(oR.dGroupFields, Group, 0)
    if "edit-group" in oR.oArgs:
        oR.dGroupFields['project']['list'] = Project.select()
        oR.dGroupFields['project']['sel_value'] = oR.sSelectProject
        oR.dGroupFieldsV = fnPrepareFormFields(oR.dGroupFields, Group, oR.sEditGroup)
    if "create-task" in oR.oArgs:
        oR.dTaskFields['group']['list'] = Group.select()
        oR.dTaskFields['group']['sel_value'] = oR.sSelectGroup
        oR.dTaskFieldsV = fnPrepareFormFields(oR.dTaskFields, Task, 0)
    if "edit-task" in oR.oArgs:
        oR.dTaskFields['group']['list'] = Group.select()
        oR.dTaskFields['group']['sel_value'] = oR.sSelectGroup
        oR.dTaskFieldsV = fnPrepareFormFields(oR.dTaskFields, Task, oR.sEditTask)

    if "save-project" in oR.oArgs:
        fnPrepareFormArgs()
        Project.create()

    # print(oR.oGroups[0].name)
    oR.lTasks = []
    for oGroup in oR.oGroups:
        oR.lTasks.append(Task.select().where(Task.group==oGroup.id).order_by(-Task.sort))

@app.route("/", methods=['GET', 'POST'])
@cache.cached()
def index():
    oIndex = Notes.get(Notes.name=='index')
    return render_template(
        'index.html', 
        oIndex=oIndex
    )

@app.route("/get_file/<id>", methods=['GET', 'POST'])
@cache.cached()
def get_file(sID):
    oFile = File.get_by_id(sID)
    oR = Response(readfile(oFile.path), mimetype=mimetypes.guess_type(oFile.path)[0])
    oR.headers['Cache-Control'] = 'max-age=60480000, stale-if-error=8640000, must-revalidate'
    return oR

@app.route("/projects", methods=['GET', 'POST'])
@cache.cached()
def projects():
    oR = RequestVars()
    fnPrepareProjectsData(oR)

    return render_template(
        'projects.html', 
        oR=oR 
    )

@app.route("/all_tasks", methods=['GET', 'POST'])
@cache.cached()
def all_tasks():
    oR = RequestVars()
    fnPrepareProjectsData(oR)

    oR.lAllTasks = Task.select()

    return render_template(
        'project_list_all.html',
        oR=oR
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

@app.route("/dictionary", methods=['GET', 'POST'])
@cache.cached()
def dictionary():
    return render_template(
        'dictionary.html', 
    )

@app.route("/links_database", methods=['GET', 'POST'])
@cache.cached()
def links_database():
    return render_template(
        'links_database.html', 
    )

def run():
    print("[!] RUN ON HOST 0.0.0.0")
    app.run(host='0.0.0.0')

if __name__ == "__main__":
    run()