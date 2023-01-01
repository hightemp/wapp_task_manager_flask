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
from playhouse.shortcuts import model_to_dict
import zipfile
from flask_caching import Cache

# NOTE: Константы
UPLOAD_PATH_REL = "static/uploads"
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), UPLOAD_PATH_REL)
DATABASE = './wapp_task_manager_flask.database.db'

__DEMO__ = True
__DEBUG__ = False

if (__DEMO__):
    os.unlink(DATABASE)

# NOTE: Переменные
bFirstStart = not os.path.exists(DATABASE)
print("[!] INIT APP DATABASE=", DATABASE, " bFirstStart=", bFirstStart)
app = Flask(__name__)
config = {
    # "DEBUG": True,          # some Flask specific configs
    # "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)
db = SqliteDatabase(DATABASE)

# NOTE: Модели
class Project(Model):
    name = CharField()
    sort = IntegerField(default=0)

    class Meta:
        database = db

class Group(Model):
    name = CharField()
    sort = IntegerField(default=0)
    project = ForeignKeyField(Project, backref='groups')
    color = CharField()

    class Meta:
        database = db

class Task(Model):
    name = CharField()
    sort = IntegerField(default=0)
    group = ForeignKeyField(Group, backref='tasks')
    a_html = TextField(null=True)
    a_markdown = TextField(null=True)
    created_at = DateField(default=datetime.datetime.now)
    updated_at = DateField(default=datetime.datetime.now)

    class Meta:
        database = db

class File(Model):
    name = CharField()
    sort = IntegerField(default=0)
    path = CharField()

    class Meta:
        database = db

class Notes(Model):
    name = CharField()
    sort = IntegerField(default=0)
    a_html = TextField(null=True)
    a_markdown = TextField(null=True)
    created_at = DateField(default=datetime.datetime.now)
    updated_at = DateField(default=datetime.datetime.now)

    class Meta:
        database = db

db.connect()

def readfile(sFilePath):
    if (__DEBUG__):
        return open(sFilePath, 'rb').read()
    else:
        with zipfile.ZipFile(os.path.dirname(__file__)) as z:
            # print(z.namelist())
            with z.open(sFilePath) as f:
                print("[!] "+f.name)
                # print("[!] "+f.read().decode("utf-8"))
                return f.read()
        return "ERROR"

def load_template(name):
    return readfile("templates/"+name).decode("utf-8")

oTempFunctionLoader = FunctionLoader(load_template)

def render_template(name, **kwargs):
    if __DEBUG__:
        return render_template_default(name, **kwargs)
    else:
        data = load_template(name)
        tpl = Environment(loader=oTempFunctionLoader).from_string(data)
        return tpl.render(**kwargs)

if (bFirstStart):
    print("[!] FIRST START")
    db.create_tables([Project, Group, Task, File, Notes])

    if (__DEMO__):
        sHTML = """
<ul>
    <li>FDTD — это простой и интуитивно понятный метод.
    <li>Поскольку FDTD работает во временной области, он позволяет получить результат для широкого спектра длин волн за один расчет. Это может быть полезно при решении задач, в которых не известны резонансные частоты или в случае моделирования широкополосных сигналов.
    <li>FDTD позволяет создавать анимированные изображения распространения волны в моделируемом объеме.
    <li>FDTD удобен при задании анизотропных, дисперсных и нелинейных сред.
    <li>Метод позволяет непосредственно моделировать краевые эффекты и эффекты экранирования, причем поля внутри и вне экрана могут быть рассчитаны как напрямую, так и нет.
</ul>
"""
        project01 = Project.create(name='Тестовый проект 1')

        group01 = Group.create(name="todo", color="#aeb5ff", project=project01)
        group02 = Group.create(name="doing", color="#c1f186", project=project01)
        group03 = Group.create(name="done", color="#d3d3d3", project=project01)

        task01 = Task.create(name="Проект - дизайн", group=group01, a_html=sHTML)
        task02 = Task.create(name="Проект - доработка", group=group01, a_html=sHTML)
        task03 = Task.create(name="Перенести задачи из старого таск менеджера", group=group01, html=sHTML)
        task04 = Task.create(name="Проект - Задача 04", group=group01, a_html=sHTML)

        task05 = Task.create(name="Проект - Задача 05", group=group02, a_html=sHTML)
        task06 = Task.create(name="Проект - Задача 06", group=group02, a_html=sHTML)
        
        task07 = Task.create(name="Проект - Задача 07", group=group03, a_html=sHTML)

        project02 = Project.create(name='Тестовый проект 2')
        project03 = Project.create(name='Тестовый проект 3')
        project04 = Project.create(name='Тестовый проект 4')

        sIndexPage = readfile("templates/README/index.html")
        Notes.create(name="index", a_html=sIndexPage)

def models_col_to_list(lModelsCol):
    lList = []
    for oA in lModelsCol:
        lList.append(model_to_dict(oA))

    return lList

# NOTE: Хелперы
def parse_get(args):
    data = {}

    for u, v in args.lists():
        if hasattr(v, "__len__"):
            for k in v:
                data[u] = k
                if k == '':
                    del data[u]
        else:
            data[u] = v
            if v == '':
                del data[u]

    return data

def parse_multi_form(form):
    data = {}
    for url_k, v in form.lists():
        if ('' in v):
            continue
        v = v[0]

        ks = []
        while url_k:
            if '[' in url_k:
                k, r = url_k.split('[', 1)
                ks.append(k)
                if r[0] == ']':
                    ks.append('')
                url_k = r.replace(']', '', 1)
            else:
                ks.append(url_k)
                break
        sub_data = data
        for i, k in enumerate(ks):
            if k.isdigit():
                k = int(k)
            if i+1 < len(ks):
                if not isinstance(sub_data, dict):
                    break
                if k in sub_data:
                    sub_data = sub_data[k]
                else:
                    sub_data[k] = {}
                    sub_data = sub_data[k]
            else:
                if isinstance(sub_data, dict):
                    sub_data[k] = v

    return data

# @cache.cached(timeout=500)
# def fnIterCategories(iGroupID, aOpened, sCategoryFilter, aCategories=[], iLevel=0):
#     if (iLevel==0):
#         aQueryCategories = []

#         if str(iGroupID)=="-1":
#             aQueryCategories = Category.select().where(Category.name ** f"%{sCategoryFilter}%", Category.parent == None)
#         else: 
#             aQueryCategories = Category.select().where(Category.name ** f"%{sCategoryFilter}%", Category.parent == None, Category.group == iGroupID)

#         return fnIterCategories(iGroupID, aOpened, sCategoryFilter, aQueryCategories, 1)
#     else:
#         aNewCategories = []
#         for oCategory in aCategories:
#             sID = oCategory.id

#             if str(iGroupID)=="-1":
#                 aQueryCategories = Category.select().where(Category.name ** f"%{sCategoryFilter}%", Category.parent == sID)
#             else: 
#                 aQueryCategories = Category.select().where(Category.name ** f"%{sCategoryFilter}%", Category.parent == sID, Category.group == iGroupID)
            
#             if sCategoryFilter!='':
#                 aQueryCategories.where(Category.name ** f"%{sCategoryFilter}%")

#             aIterCategories = []
#             if (sID in aOpened) and aQueryCategories and len(aQueryCategories)>0:
#                 aIterCategories = fnIterCategories(iGroupID, aOpened, sCategoryFilter, aQueryCategories, iLevel+1)
            
#             iCnt = Account.select().where(Account.category == sID).count()

#             oNewCategory = {}
#             oNewCategory['id'] = oCategory.id
#             oNewCategory['name'] = oCategory.name
#             oNewCategory['level'] = (iLevel - 1) * "<span class='tree-spacer'></span>" + oNewCategory['name']
#             oNewCategory['cnt'] = iCnt

#             aNewCategories += [oNewCategory] + aIterCategories
        
#         return aNewCategories

class RequestVars:
    dProjectFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сорт',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
    }

    dGroupFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сорт',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
        'project': {
            'name': 'Проект',
            'type': 'select',
            'field_name': 'project',
            'list': [],
            'value': '',
        },
    }

    dTaskFields = {
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сорт',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
        'a_html': {
            'name': 'Описание HTML',
            'type': 'textarea',
            'field_name': 'a_html',
            'value': '',
        },
        'a_markdown': {
            'name': 'Описание Markdown',
            'type': 'textarea',
            'field_name': 'a_markdown',
            'value': '',
        },
    }

    dClasses = {
        'group': 'Group',
        'category': 'Category',
        'account': 'Account',
    }

    aProjectsButtons = [
        {"name":"reload", "cls":"bi-arrow-repeat", "btn_cls": "btn-primary"},
        {"name":"create_project", "cls":"bi-file-plus", "btn_cls": "btn-success"},
        {"name":"edit_project", "cls":"bi-pencil", "btn_cls": "btn-secondary"},
        {"name":"remove_project", "cls":"bi-trash", "btn_cls": "btn-danger"},
    ]

    aArgsAssoc = {
        "select-project": "sSelectProject",
        "select-group": "sSelGroup",
        "select-task": "sSelTask",
        "edit-group": "sEditGroup",
        "edit-group": "sEditGroup",
    }

    sGroupFilter = ''
    sCategoryFilter = ''
    sAccountFilter = ''

    oProjects={}
    oGroups={}
    lTasks = []

    oProject={}
    oGroup={}
    oTask={}

    sBaseURL = ""

    sSelectProject = ""
    sSelectGroup = ""
    sSelectTask = ""
    sSelectFile = ""

    sEditGroup = ""
    sEditTask = ""

def fnPrepareFormFields(aFields, cCls, sSelID):
    kls = globals()[cCls]
    oItem = {}
    if sSelID != "" and int(sSelID) > 0:
        try:
            oItem = kls.get_by_id(sSelID)
            oItem = model_to_dict(oItem, recurse=False, backrefs=False)
        except:
            pass

    for sK, oV in aFields.items():
        if 'sel_value' in aFields[sK]:
            aFields[sK]['value'] = aFields[sK]['sel_value']
        else:
            if sSelID==0:
                aFields[sK]['value'] = ''
            else:
                if sK in oItem and oItem[sK]:
                    aFields[sK]['value'] = oItem[oV['field_name']]
                else:
                    aFields[sK]['value'] = ''
    return aFields

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