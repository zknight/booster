import os, sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('../doc/booster.cfg.default')
app.config.from_pyfile('../booster.cfg', silent=True)

db = SQLAlchemy(app)

from booster.stuff import *
import booster.views
import booster.models
from booster.util import *
