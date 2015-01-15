import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from booster import db
from booster.models import User, Event, EventType

#db.drop_all()
#db.create_all()

if len(sys.argv) != 4:
    print "Usage: init-db.py <login> <email> <password>"
    exit(1)

login = sys.argv[1]
email = sys.argv[2]
password = sys.argv[3]

print "Creating admin '{0}' with email '{1}' and password '{2}'".format(
        login, email, password)
admin = User(login, password, email, True)
db.session.add(admin)
db.session.commit()

