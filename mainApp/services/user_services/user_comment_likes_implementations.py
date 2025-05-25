from flask import jsonify
from models.Blog_Comment_model import Blog_Comment
from models.Blog_model import Blog
from models.Users_model import Users
from models.db import db
import re


def user_comment_likes_implementations(email, username, like_comment_id):

    try:
        if not email:
            return "email filed must be filled"
        elif not username:
            return "username filed must be filled"
        elif not like_comment_id:
            return "like_comment_id filed must be filled"
        is_valid_email = re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email
        )
        if not is_valid_email:
            return "invalid email"
        blog_comment = Blog_Comment.query.get(like_comment_id)
        if not blog_comment:
            return "comment not found"
        
        for like_user in blog_comment.comment_like_user_relation:
            if like_user.email == email:
                return "user is already like the comment"
            
        user = Users(email=email, username=username)
        db.session.add(user)
        blog_comment.comment_like_user_relation.append(user)
        db.session.commit()

        return {
                "email": user.email,
                "username": user.username,
                "comment_id": blog_comment.id,
            }
    except Exception as e:
        print(f"Error at user_comment_likes_implementations {str(e)}")
        return f"Error : {str(e)}"
