from flask import Flask, jsonify, request
from models.Blog_model import Blog
import re
from services.user_services.get_user_comments_implementation import (
    user_likes,
    get_user_comment_list,
)
from services.user_services.user_comment_likes_implementations import (
    user_comment_likes_implementations,
)
from services.user_services.like_dislike_implementation import (
    like_id_implementation,
    dislike_id_implementation,
)
from services.user_services.sub_user_comments_implementations import (
    sub_user_comments_implementations,
)
from services.user_services.comments_implementaion import comment_implementations


# blog
def blog(page, per_page):

    try:
        blogs = Blog.query.paginate(page=page, per_page=per_page)
        blog_data = []
        for blog in blogs:
            blog_data.append({"id": blog.id, "post": blog.post})
        return blog_data
    except Exception as e:
        return f"Error: {str(e)}"


# comments
def comments(comment, email, username):

    try:
        if not comment:
            return "comment filed must be filled"
        elif not email:
            return "email filed must be filled"
        elif not username:
            return "username filed must be filled"
        is_valid_email = re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        if not is_valid_email:
            return "invalid email"
        data = comment_implementations(comment, email, username)
        if isinstance(data, tuple):
            return data
        return data
    except Exception as e:
        return f"Error: {str(e)}"


# sub_user_comments
def sub_user_comments(email, username, sub_comment, parent_id):

    try:
        if not sub_comment:
            return "comment filed must be filled"
        elif not email:
            return "email filed must be filled"
        elif not username:
            return "username filed must be filled"
        elif not parent_id:
            return "parent_id filed must be filled"
        is_valid_email = re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        if not is_valid_email:
            return "invalid email"
        data = sub_user_comments_implementations(
            email, username, sub_comment, parent_id)
        if isinstance(data, tuple):
            return data
        return data
    except Exception as e:
        return f"Error: {str(e)}"


# like_dislike_blog
def like_dislike_blog(like_id, dislike, email, username):

    try:
        if not email:
            return "email filed must be filled"
        elif not username:
            return "username filed must be filled"
        is_valid_email = re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        if not is_valid_email:
            return "invalid email"
        if like_id:
            data = like_id_implementation(email, username, like_id)
            if isinstance(data, (tuple, str, dict, list)):
                return data
        elif dislike:
            data = dislike_id_implementation(email, dislike)
            if isinstance(data, (tuple, str, dict, list)):
                if data == "dislike the post":
                    return data
                elif data == "like the post first":
                    return data
        return "like_id or dislike not found "
    except Exception as e:
        response = f"Error at like_dislike_blog{e}"
        return f"Error: {str(e)}"


# user_comment_likes
def user_comment_likes(email, username, like_comment_id):

    try:
        data = user_comment_likes_implementations(email, username, like_comment_id)
        if isinstance(data, tuple):
            return data
        return data
    except Exception as e:
        print(f"DEBUG: Error at user comment likes {str(e)}")
        response = f"error {str(e)}"
        return response


# get_user_comments
def get_user_comments(page, per_page):

    try:
        like_list = user_likes()
        if isinstance(like_list, tuple):
            return "like_list error"
        like_list
        comment_list = get_user_comment_list(page, per_page)
        if isinstance(comment_list, tuple):
            return comment_list
        comment_list
        blog = Blog.query.first()
        if not blog:
            return "blog not found"
        return {
            "post": blog.post,
            "likes": like_list,
            "comments": comment_list,
        }

    except Exception as e:
        response = f"Error  at get_user_comments {e}"
        return f"Error: {str(e)}"
