from models.db import db

class Blog(db.Model):
    __tablename__="blog"
    id = db.Column(db.Integer,primary_key=True)
    post = db.Column(db.String(), nullable = False)
