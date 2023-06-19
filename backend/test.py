from email.mime import application
from application import db
from application import application

with application.app_context():
    db.create_all()