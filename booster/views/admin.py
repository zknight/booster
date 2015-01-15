from booster import app, db
from booster.models import User, Event, EventType
from flask import render_template, url_for, redirect, session, flash
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *
#from wtforms.validators import ValidationError
from flask.ext.wtf import Form
from booster.stuff import protected
from datetime import datetime, date
#from booster.util import parse_time
from formstuff import TimeField, DateValidator, TimeValidator

@app.route("/admin")
@protected()
def admin_index():
    events = Event.query.all()
    users = User.query.all()
    return render_template("admin/index.html", events = events, users = users)

# TODO: Test this. Don't know if it above will work. Trying to implement a decorator,
# may fail.
    #if 'loggedin' in session and session['loggedin']:
        #events = Event.query.all()
        #users = User.query.all()
        #return render_template("admin/index.html", events = events, users = users)
    #else:
        #flash('Guess what. You are not logged in. And I am not telling you how.' \
                #'You should know if you have access.')
        #return redirect(url_for('index'))


@app.route("/notabackdoor", methods=['GET', 'POST'])
def admin_login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        login = login_form.login.data
        password = login_form.password.data
        user = User.query.filter(User.login == login).first()
        session['loggedin'] = True
        session['user'] = user.id
        flash('You are now logged in.')
        return redirect(url_for('admin_index'))

    return render_template("admin/login.html", login_form = login_form)

@app.route("/logout")
def admin_logout():
    if 'loggedin' in session:
        session.pop('loggedin')
        session.pop('user')
    return redirect(url_for('index'))

##############
# User actions
############## 
@app.route("/admin/user/edit/<login>", methods=['GET', 'POST'])
@protected()
def edit_user(login):
    u = User.query.filter(User.login == login).first() 
    if not u:
        return redirect(url_for('admin_index'))
    user_form = UserForm(obj=u)
    
    if user_form.validate_on_submit():
        # TODO: modify user in db
        u.login = user_form.login.data
        u.password = user_form.password.data
        u.email = user_form.email.data
        db.session.commit()
        return redirect(url_for('admin_index'))

    return render_template("admin/user_form.html",
            user_form = user_form,
            action = url_for('edit_user', login=login))

@app.route("/admin/user/delete/<login>")
@protected("index")
def delete_user(login):
    u = User.query.filter(User.login == login).first()
    if not u:
        flash("No user with login: {0}".format(login))
    elif u.is_super:
        flash("Can't delete your Super User!")
    else:
        db.session.delete(u)
        db.session.commit()
        flash("User {0} deleted.".format(login))

    return redirect(url_for('admin_index'))

@app.route("/admin/user/add", methods=['GET', 'POST'])
@protected("index")
def add_user():
    user_form = UserForm()

    if user_form.validate_on_submit():
        new_user = User(
                user_form.login.data,
                user_form.password.data,
                user_form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash("User {0} added.".format(new_user.login))
        return redirect(url_for('admin_index'))

    return render_template("admin/user_form.html", 
            user_form = user_form, 
            action = url_for('add_user'))

############ 
# User Forms
############ 
class LoginValidator(object):
    def __init__(self, pw_field, message_login = "The login or password is incorrect.",
            message_password = "The login or password is incorrect."):
        self.pw_field = pw_field
        self.message_login = message_login
        self.message_password = message_password

    def __call__(self, form, field):
        u = User.query.filter(User.login == field.data).first()
        if not u:
            raise ValidationError(self.message_login)
        elif not u.authorize(form[self.pw_field].data):
            raise ValidationError(self.message_password)

class UserValidator(object):
    def __init__(self, message_login = "This login already exists."):
        self.message_login = message_login

    def __call__(self, form, field):
        u = None
        if field.data:
            u = User.query.filter(User.login == field.data).first()
        if u:
            raise ValidationError(self.message_login)

class EmailValidator(object):
    def __call__(self, form, field):
        u = User.query.filter(User.email == field.data).first()
        if u:
            raise ValidationError("A user with this email already exists.")

class LoginForm(Form):
    login = TextField("Login", validators=[LoginValidator("password")])
    password = PasswordField("Password", validators = [])

class UserForm(Form):
    login = TextField("Login", validators=[
        UserValidator(), 
        Length(min=3, max=64, 
            message="Login must have at least 3 characters but no more than 80"),
        Regexp(("[0-9a-zA-Z\-_]"), message="Login contains invalid characters." \
                " Allowed characters: alphanumeric, '-', and '_'")
        ])

    email = TextField("Email", validators=[
        EmailValidator(), 
        DataRequired("Email is required"),
        Email("Email appears invalid")
        ])

    password = PasswordField("Password", validators=[
        EqualTo('confirm', message='Password and cofirmation must match')
        ])

    confirm = PasswordField("Confirm Password")

###############
# Event actions
###############
@app.route("/admin/event/edit/<eid>", methods=['GET', 'POST'])
@protected()
def edit_event(eid):
    e = Event.query.filter(Event.id == eid).first()
    if not e:
        return redirect(url_for('admin_index'))
    event_form = EventForm(obj=e)

    if event_form.validate_on_submit():
        start_date = event_form.start_date.data
        start_time = event_form.start_time.data
        end_date = event_form.end_date.data
        end_time = event_form.end_time.data

        e.name = event_form.name.data
        e.text = event_form.text.data
        e.start_time = datetime.combine(start_date, start_time)
        e.end_time = datetime.combine(end_date, end_time)
        e.event_type = event_form.event_type.data
        db.session.commit()
        return redirect(url_for('admin_index'))

    return render_template("admin/event_form.html",
            event_form = event_form,
            action = url_for('edit_event', eid = e.id))

@app.route("/admin/event/delete/<eid>")
@protected("index")
def delete_event(eid):
    e = Event.query.filter(Event.id == eid).first()
    if not e:
        flash("No valid event with that id.")
    else:
        db.session.delete(e)
        db.session.commit()
        flash("Event deleted.")
    return redirect(url_for('admin_index'))

@app.route("/admin/event/add", methods=['GET', 'POST'])
@protected("index")
def add_event():
    event_form = EventForm()

    event_form.event_type.choices = [(et.id, et.name) \
            for et in EventType.query.order_by('name')]

    if event_form.validate_on_submit():
        start_date = event_form.start_date.data
        start_time = event_form.start_time.data
        end_date = event_form.end_date.data
        end_time = event_form.end_time.data

        new_event = Event(
                event_form.name.data,
                event_form.text.data,
                datetime.combine(start_date, start_time),
                datetime.combine(end_date, end_time),
                event_form.event_type.data)

        db.session.add(new_event)
        db.session.commit()
        flash("Event {0} added.".format(new_event.name))
        return redirect(url_for('admin_index'))

    return render_template("admin/event_form.html",
            event_form = event_form,
            action = url_for('add_event'))

@app.route("/admin/event/types")
@protected("index")
def manage_event_types():
    event_types = EventType.query.all()
    return render_template("admin/event_types.html", event_types = event_types)

@app.route("/admin/event/types/add", methods=['GET', 'POST'])
@protected("index")
def add_event_type():
    event_type_form = EventTypeForm()

    if event_type_form.validate_on_submit():
        new_et = EventType(
                event_type_form.name.data,
                event_type_form.name.description)
        db.session.add(new_et)
        db.session.commit()
        flash("EventType {0} created.".format(new_et.name))
        return redirect(url_for('manage_event_types'))

    return render_template("admin/event_type_form.html",
            event_type_form = event_type_form,
            action = url_for('add_event_type'))

@app.route("/admin/event/types/delete/<etid>")
@protected("index")
def delete_event_type(etid):
    et = EventType.query.filter(EventType.id == etid).first()
    if not et:
        flash("No valid event type with that id.")
    else:
        db.session.delete(et)
        db.session.commit()
        flash("Event deleted.")
    return redirect(url_for('manage_event_types'))

#############
# Event Forms
#############
class EventForm(Form):
    event_type = SelectField("Event Type", coerce=int)
    name = TextField("Event Name", validators=[
        Length(min=3, max=64,
            message="Name must have at least 3 characters but no more than 64"),
        Regexp(("[0-9a-zA-Z\-_]"), message="Event name contains non-alphanumeric characters")
            ])

    text = TextAreaField("Event Description", validators=[InputRequired(message="Text Input Required")])

    start_date = DateField("Start Date (YYYY-MM-DD)", 
            validators=[DateValidator()],
            format='%Y-%m-%d'
            )

    start_time = TimeField("Start Time", validators=[TimeValidator()])

    end_date = DateField("End Date (YYYY-MM-DD)",
        validators=[DateValidator("start_date", lambda ed, sd: ed >= sd, 
            "End date must be the same or come after the start date")],
            format='%Y-%m-%d'
            )

    end_time = TimeField("End Time", validators=[TimeValidator()])

class EventNameValidator(object):
    def __call__(self, form, field):
        et = None
        if field.data:
            et = EventType.query.filter(EventType.name == field.data).first()
        if et:
            raise ValidationError("An Event Type with that name already "
                    " exists.")

class EventTypeForm(Form):
    name = TextField("Event Type", validators=[
        Length(min=3, max=64,
            message="Name must have at least 3 characters but no more than 64"),
        Regexp(("[0-9,a-zA-Z\=_]"), message="Event name contains "
            "non-alphanumeric characters"),
        EventNameValidator()
        ])

    description = TextAreaField("Event Type Description",
            validators=[InputRequired(message="Text Input Required")])
