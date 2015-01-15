#!/usr/bin/env python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Command
from flask.ext.migrate import Migrate, MigrateCommand
import sys

app = Flask(__name__)

app.config.from_pyfile('doc/booster.cfg.default')
app.config.from_pyfile('booster.cfg', silent=True)
print app.config['SQLALCHEMY_DATABASE_URI']

db = SQLAlchemy(app)
import booster
from booster.models import *

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class ShowModels(Command):
    def run(self):
        global db
        for t in db.metadata.sorted_tables:
            print t.name
        #print db.metadata.tables.keys()
        #for x in dir(db): print x
        #print dir(booster.models)

class RunServer(Command):
    def run(self):
        from booster import app
        app.run(host="0.0.0.0")

manager.add_command('models', ShowModels)
manager.add_command('server', RunServer)

if __name__ == '__main__':
    manager.run()

