import os
from peewee import *
import datetime
from baselib import *

UPLOAD_PATH_REL = "static/uploads"
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), UPLOAD_PATH_REL)
DATABASE = './wapp_task_manager_flask.database.db'

__DEMO__ = True

# if (__DEMO__):
#     os.unlink(DATABASE)

bFirstStart = not os.path.exists(DATABASE)
db = SqliteDatabase(DATABASE)
lClasses = []

# NOTE: Модели
class Project(Model):
    name = CharField()
    sort = IntegerField(default=0)

    class Meta:
        database = db
lClasses.append(Project)

class Group(Model):
    name = CharField()
    sort = IntegerField(default=0)
    project = ForeignKeyField(Project, backref='groups')
    color = CharField()

    class Meta:
        database = db
lClasses.append(Group)

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
lClasses.append(Task)

class Comment(Model):
    task = ForeignKeyField(Task, backref='tasks')
    a_html = TextField(null=True)
    a_markdown = TextField(null=True)
    created_at = DateField(default=datetime.datetime.now)
    updated_at = DateField(default=datetime.datetime.now)

    class Meta:
        database = db
lClasses.append(Comment)

class File(Model):
    name = CharField()
    sort = IntegerField(default=0)
    path = CharField()
    task = ForeignKeyField(Task, backref='tasks')

    class Meta:
        database = db
lClasses.append(File)

class Notes(Model):
    name = CharField()
    sort = IntegerField(default=0)
    a_html = TextField(null=True)
    a_markdown = TextField(null=True)
    created_at = DateField(default=datetime.datetime.now)
    updated_at = DateField(default=datetime.datetime.now)

    class Meta:
        database = db
lClasses.append(Notes)

db.connect()

# NOTE: DEMO
if (bFirstStart):
    print("[!] FIRST START")
    db.create_tables(lClasses)

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
        
        for iI in range(0, 20):
            Comment.create(task=task01, a_html="It sounds wonderful, but it's 100 percent accurate! The experiences factor is wireless. Without niches, you will lack experiences. It may seem marvelous, but it's 100% realistic! What does the buzzword 'technologies' really mean? Think granular. Our infinitely reconfigurable feature set is unparalleled, but our sexy raw bandwidth and easy operation is invariably considered a remarkable achievement. What does the term 'structuring'. Clicking on this link which refers to B2B Marketing awards shortlist will take you to the ability to whiteboard without lessening our power to aggregate. What does it really mean to e-enable 'dynamically'? We pride ourselves not only on our robust feature set, but our back-end performance and non-complex configuration is usually considered a terrific achievement. In order to assess the 3rd generation blockchain’s ability to whiteboard without lessening our power to benchmark. It may seem terrific, but it's realistic! Imagine a combination of PGP and XSL. Without efficient, transparent bloatware, you will lack affiliate-based compliance. Without development, you will lack architectures. That is a remarkable achievement taking into account this month's financial state of things! If all of this sounds astonishing to you, that's because it is! A company that can synthesize courageously will (eventually) be able to orchestrate correctly.")

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