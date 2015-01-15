from booster.util import parse_time
from wtforms.fields import *
from wtforms.widgets import *
from wtforms.validators import *
from wtforms.validators import ValidationError
from datetime import date

class TimeField(Field):
    widget = TextInput()
    parsed = False
    orig = ""

    def _value(self):
        print (self.data)
        if self.data is not None:
            #print self.data.strftime("%H:%M:%S")
            return self.data.strftime("%H:%M:%S")
        else:
            return u''

    def process_formdata(self, value_list):
        if value_list:
            self.orig = value_list[0]
            self.data = parse_time(self.orig)
            if self.data is not None:
                self.parsed = True
        else:
            self.data = None

class DateValidator(object):
    def __init__(self, cmp_field=None, cmpfunc=lambda x, y: x == y,
            msg="Invalid date"):
        self.cmp_field = cmp_field
        self.cmpfunc = cmpfunc
        self.msg = msg

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError("{0}: must not be empty".format(
                field.short_name))
        if field.data < date.today():
            raise ValidationError("{0}: can't go back in "
                    "time!".format(field.short_name))
        if self.cmp_field:
            if not self.cmpfunc(field.data, form[self.cmp_field].data):
                raise ValidationError(self.msg)


class TimeValidator(object):
    def __call__(self, form, field):
        if not field.parsed:
            raise ValidationError("{0}: {1}".format(field.short_name, field.orig))
        print field.data
        if field.data is None:
            raise ValidationError("{0}: Time must not be "
                    "empty".format(field.short_name))

