from flask import Flask
from models.Blog_Comment_model import Blog_Comment
from models.Blog_model import Blog
from models.Users_model import Users
from models.db import db
def comment_implementations(comment, email,username):

    try:
        users = Users(email=email, username=username)
        db.session.add(users)
        db.session.commit()
        blog = Blog.query.first()
        if not blog:
            return "blog not found"
        user_comment = Blog_Comment(
            text=comment, blog_id=blog.id, parent_comment_id=None)
        db.session.add(user_comment)
        user_comment.user_relation.append(users)
        db.session.commit()
        return {
            "comment": user_comment.text,
            "blog_id": blog.id,
            "comment_id": user_comment.id,}
    except Exception as e:
        print(f"Error at comment_implementations{e}")
        return f"Error: {str(e)}"

      

