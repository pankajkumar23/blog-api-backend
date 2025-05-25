from flask import Flask
from models.Likes_model import Likes
from models.Users_model import Users
from models.db import db


def like_id_implementation(email, username, like_id):

    try:
        if like_id:
            existing_user = Users.query.filter_by(email=email).first()
            if existing_user:
                return "user already liked the blog"
            update_users = Users(email=email, username=username)
            db.session.add(update_users)
            db.session.commit()
            like = Likes(user_likes_id=update_users.id)
            db.session.add(like)
            db.session.commit()
            response = True
            return {
                "username": update_users.username,
                "email": update_users.email,
                "response": response,
                "id": update_users.id,
            }
    except Exception as e:
        print(f"Error at user_comment_likes_implementations {str(e)}")
        return f"Error: {str(e)}"


def dislike_id_implementation(email, dislike):

    try:
        if dislike:
            user = Users.query.filter_by(email=email).first()
            if user:
                all_users = Users.query.all()
                for current_user in all_users:
                    for user_like in current_user.like:

                        if user_like.user_likes_id == user.id:
                            like = Likes.query.filter_by(
                                user_likes_id=user_like.user_likes_id
                            ).first()
                            db.session.delete(like)
                            db.session.delete(user)
                            db.session.commit()
                            return "dislike the post"
            return "like the post first"
    except Exception as e:
        print(f"Error at user_comment_likes_implementations {str(e)}")
        return f"Error: {str(e)}"
