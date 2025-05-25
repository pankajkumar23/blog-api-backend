from models.db import db


class Users(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(),nullable = True)
    email = db.Column(db.String(),nullable = True)
   
