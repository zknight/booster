from booster import app, db
#from booster.models import
from flask import render_template, url_for, redirect, session, flash

@app.route("/store")
def store_index():
    return render_template("store.html")
