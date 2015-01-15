from booster import app, db
from booster.models import Event, EventType, News
from flask import render_template, url_for, redirect
import datetime

@app.route("/")
def index():
    upcoming_events = Event.query.filter(Event.start_time >= datetime.datetime.now()).all()
    current_news = News.get_current()
    return render_template("index.html", events=upcoming_events,
            news=current_news)

