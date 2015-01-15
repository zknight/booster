from booster import app, db
from booster.models import User, News
from flask import render_template, url_for, redirect, session, flash
from wtforms.fields import *
from wtforms.validators import *
from wtforms.validators import ValidationError
from flask.ext.wtf import Form
from booster.stuff import protected
from formstuff import TimeField, DateValidator, TimeValidator
from datetime import time, datetime

@app.route("/admin/news")
@protected("index")
def news_index():
    current_news = News.get_current()
    expired_news = News.get_expired()
    return render_template("admin/news.html", 
            current_news = current_news,
            expired_news = expired_news)

@app.route("/admin/news/add", methods=['GET', 'POST'])
@protected("index")
def add_news():
    news_form = NewsForm()
    
    if news_form.validate_on_submit():
        expiry_date = news_form.expiry_date.data
        expiry_time = news_form.expiry_time.data
        
        new_article = News(
                title = news_form.title.data,
                tease = news_form.tease.data,
                body = news_form.body.data,
                created_at = datetime.now(),
                updated_at = datetime.now(),
                expiry = datetime.combine(expiry_date, expiry_time)
                )

        db.session.add(new_article)
        db.session.commit()
        flash("Article {0} added.".format(new_article.title))
        return redirect(url_for('news_index'))

    return render_template("admin/news_form.html",
            news_form = news_form,
            action = url_for('add_news'))


@app.route("/admin/news/edit/<nid>", methods=['GET', 'POST'])
@protected("index")
def edit_news(nid):
    n = News.query.filter(News.id == nid).first()
    if not n:
        return redirect(url_for('news_index'))
    news_form = NewsForm(obj=n)

    if news_form.validate_on_submit():
        n.title = news_form.title.data
        n.tease = news_form.tease.data
        n.body = news_form.body.data
        n.updated_at = datetime.now()
#TODO: think about moving this stuff to the news class
        n.expiry = datetime.combine(
                news_form.expiry_date.data,
                news_form.expiry_time.data)
        db.session.commit()
        return redirect(url_for('news_index'))

    return render_template("admin/news_form.html",
            news_form = news_form,
            action = url_for('edit_news', nid = n.id))

@app.route("/admin/news/delete/<nid>")
@protected("index")
def delete_news(nid):
    n = News.query.filter(News.id == nid).first()
    if not n:
        flash("No valid article with that id.")
    else:
        db.session.delete(n)
        db.session.commit()
        flash("Event deleted.")
    return redirect(url_for('news_index'))

############
# News Forms
############
class NewsForm(Form):
    title = TextField("Article Title", validators=[
        Length(min=3, max=256, 
            message="Title must be at least 3 characters but less than 256"),
        Regexp(("[^<>]"), message="Title Cannot contain angle brackets")
        ])

    tease = TextAreaField("Article Intro", validators=[
        InputRequired(message="What is an article without an intro? Please add.")])

    body = TextAreaField("Article Body")

    expiry_date = DateField("Expiry Date (YYYY-MM-DD)",
            validators=[DateValidator()],
            format='%Y-%m-%d'
            )

    expiry_time = TimeField("Expiry Time", validators=[
        TimeValidator()], default = lambda: time(0))
    #expiry = DateTimeField

