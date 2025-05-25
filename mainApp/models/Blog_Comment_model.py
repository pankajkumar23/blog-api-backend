from models.db import db
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import relationship


blog_comment_user=db.Table("blog_comment_user",
 db.Column("user_id", db.Integer,ForeignKey("users.id"),primary_key=True),db.Column("user_comment_id", db.Integer,ForeignKey("blog_comment.id"),primary_key=True))


comment_like_user = db.Table("comment_like_user",
 db.Column("user_id", db.Integer,ForeignKey("users.id"),primary_key=True),db.Column("user_comment_like_id", db.Integer,ForeignKey("blog_comment.id"),primary_key=True))

class Blog_Comment(db.Model):
    __tablename__= "blog_comment"
    id = db.Column(db.Integer,primary_key=True)
    text = db.Column(db.String(), nullable = False)
    blog_id = db.Column(db.Integer, ForeignKey("blog.id"), nullable=False)
    parent_comment_id = db.Column(db.Integer, ForeignKey("blog_comment.id"), nullable=True)
    parent_comment = relationship("Blog_Comment", remote_side=[id], backref="replies")
    blog_relation = relationship("Blog", backref="blog_comments")  
    user_relation = relationship("Users", secondary = blog_comment_user, backref="comments")
    comment_like_user_relation = relationship("Users", secondary = comment_like_user, backref="comment_likes")
    
