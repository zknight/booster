from booster import app
from functools import wraps
from flask import redirect, url_for, session, flash
from datetime import date

def protected(bounce_to='index'):
    def decorator(method):
        @wraps(method)
        def f(*args, **kwargs):
            #print session
            #if not ('loggedin' in session and session['loggedin']):
            if not logged_in():
                flash("Not Authorized.")
                return redirect(url_for(bounce_to))
            return method(*args, **kwargs)
        return f
    return decorator

def logged_in():
    return 'loggedin' in session and session['loggedin']

@app.template_filter('datetime')
def format_datetime(dt, format="short"):
    if format == 'long':
        fmt = "%I:%M %p %a, %b %d %Y"
    else: 
        fmt = "%m-%d-%Y %H:%M"
        
    return dt.strftime(fmt)

@app.template_filter('bool')
def format_boolean(val, format="yesno"):
    out = ""
    if format == 'yesno':
        if val:
            out = 'Yes'
        else:
            out = 'No'
    else:
        if val:
            out = 'True'
        else:
            out = 'False'
    return out

@app.template_filter('money')
def format_money(val):
    return "${0:,.2f}".format(val)

@app.context_processor
def current_date():
    d = date.today()
    return dict(
            curyear = d.year,
            curmonth = d.month,
            curday = d.day
            )

