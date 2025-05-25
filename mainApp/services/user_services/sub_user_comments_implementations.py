from flask import jsonify, request
from models.Blog_Comment_model import Blog_Comment
from models.Blog_model import Blog
from models.Users_model import Users
from models.db import db


def sub_user_comments_implementations(email, username, sub_comment, parent_id):

    try:
        update_users = Users(email=email, username=username)
        db.session.add(update_users)
        db.session.commit()
        if parent_id:
            parent_comment = Blog_Comment.query.filter_by(id=parent_id).first()
            if not parent_comment:
                return "parent comment not found"
        blog = Blog.query.first()
        if not blog:
            return "blog not found"
        users_comment = Blog_Comment(
            text=sub_comment,
            blog_id=blog.id,
            parent_comment_id=parent_id,
        )
        db.session.add(users_comment)
        db.session.commit()
        users_comment.user_relation.append(update_users)
        db.session.commit()
        return {
            "email": update_users.email,
            "username": update_users.username,}
    except Exception as e:
        response = f"Error at sub_user_comments_implementations{e}"
        return f"Error: {str(e)}"
