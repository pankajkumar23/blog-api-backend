from models.db import db
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import relationship


class Likes(db.Model):
    __tablename__="likes"
    id = db.Column(db.Integer,primary_key=True)
    user_likes_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=True)
    user_likes = relationship("Users", backref="like") 


