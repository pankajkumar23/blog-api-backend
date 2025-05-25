from flask import Flask, Blueprint, jsonify, request
from services.user_services.user_services import (
    blog,
    comments,
    get_user_comments,
    sub_user_comments,
    like_dislike_blog,
    user_comment_likes,
)

app = Flask(__name__)
user_router = Blueprint("user", __name__)


# Blog
@user_router.route("/blog", methods=["GET"])
def user_blog():
    try:
        page = request.args.get("page", type=int)
        per_page = request.args.get("per_page", type=int)
        if page is None or per_page is None:
            return jsonify({"message": "page parameters are required!!"}), 400
        data = blog(page,per_page)
        if isinstance(data, tuple):
            return data
        elif isinstance(data,str):
            return jsonify({"message":data}),400
        elif isinstance(data, list):  
            return jsonify({"blogs": data}), 200
    except Exception as e:
        response = f"Error at user_blog {e}"
        return jsonify({"message ": response}), 400


# user_comments
@user_router.route("/comments", methods=["post"])
def user_comments():
    try:
        data = request.get_json()
        if not data:
            return "invalid json data"
        comment = data["comment"].strip()
        email = data["email"].strip()
        username = data["username"].strip()
        data = comments(comment, email,username)
        if isinstance(data, tuple):
            return data
        elif isinstance(data,dict):
            return jsonify({"message":data}),200
        elif isinstance(data,str):
            return jsonify({"message":data}),400
    except Exception as e:
        response = f"Error at user_comments {e}"
        return jsonify({"message ": response}), 400


# sub_user_comments
@user_router.route("/sub-user-comments", methods=["POST"])
def sub_all_users_comments():
    try:  
        data = request.get_json()
        if not data:
            return "invalid json data"
        email = data["email"].strip()
        username = data["username"].strip()
        sub_comment = data.get("comment")
        parent_id = data.get("parent_comment_id")
        data = sub_user_comments(email,username,sub_comment ,parent_id)
        if isinstance(data, tuple):
            return data
        elif isinstance(data,dict):
            return jsonify({"message":data}),200
        elif isinstance(data,str):
            return jsonify({"message":data}),400
    except Exception as e:
        response = f"Error at sub_all_users_comments {e}"
        return jsonify({"message ": response}), 400


# user_like_dislike_blog
@user_router.route("/like-dislike-blog", methods=["POST"])
def user_like_dislike_blog():
    try:  
        data = request.get_json()
        if not data:
            return "invalid json data"
        like_id = data.get("like_blog")
        dislike = data.get("dislike_blog")
        email = data["email"].strip()
        username = data["username"].strip()
        data = like_dislike_blog(like_id,dislike,email,username)
        if isinstance(data, tuple):
            return data
        elif isinstance(data,dict):
            return jsonify({"message":data}),200
        elif isinstance(data,str):
            if data == "dislike the post":
                response = False
                return jsonify({"like":response})
            elif data== "like the post first":
                return jsonify({"message":data}),200
        return jsonify({"message":data}),200
    except Exception as e:
        response = f"Error at user_like_dislike_blog {e}"
        return jsonify({"message ": response}), 400


@user_router.route("/user-comment-likes", methods=["POST"])
def comment_likes():
    try:
        data = request.get_json()
        if not data:
            return "invalid json data"
        email = data["email"].strip()
        username = data["username"].strip()
        like_comment_id = data.get("like_comment_id")
        data = user_comment_likes(email,username,like_comment_id)
        if isinstance(data, tuple):
            return data
        elif isinstance(data,dict):
            return jsonify({"message":data}),200
        elif isinstance(data,str):
            return jsonify({"message":data}),400
    except Exception as e:
        response = f"Error at comment_likes {e}"
        return jsonify({"message ": response}), 400


# get_user_comments
@user_router.route("/get-user-comments", methods=["GET"])
def get_all_users_comments():
    try:
        page = request.args.get("page", type=int)
        per_page = request.args.get("per_page", type=int)
        if page is None or per_page is None:
            return jsonify({"message": "page parameters are required!!"}), 400
        data = get_user_comments(page, per_page)
        if isinstance(data, tuple):
            return data
        elif isinstance(data,dict):
            return jsonify({"message":data}),200
        elif isinstance(data,str):
            return jsonify({"message":data}),400
    except Exception as e:
        response = f"Error at get_all_users_comments {e}"
        return jsonify({"message ": response}), 400
