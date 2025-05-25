from flask import jsonify, request
from models.Likes_model import Likes
from models.Users_model import Users
from models.Blog_Comment_model import Blog_Comment


# finding the users who like on blog
def user_likes():
    try:
        likes_list = []
        likes = Likes.query.all()
        for like in likes:
            user_like = like.user_likes
            likes_list.append({"username": user_like.username, "user_id": user_like.id})
        return likes_list
    except Exception as e:
        print(f"Error at user_likes {str(e)}")
        return f"Error: {str(e)}"


# finding the users who like comment on blog
def get_like_comment_user(page, per_page):

    try:
        like_comment_user_data = {}
        blog_comments = Blog_Comment.query.paginate(page=page, per_page=per_page)
        for blog_comment in blog_comments:
            for comment_like_user in blog_comment.comment_like_user_relation:
                for comment_like in comment_like_user.comment_likes:
                    like_comment_data = {
                        "username": comment_like_user.username,
                        "id": comment_like_user.id,}
                    
                    comment_like_id = comment_like.id
                    if comment_like_id not in like_comment_user_data:
                        like_comment_user_data[comment_like_id] = []
                    like_comment_user_data[comment_like_id].append(like_comment_data)
        return like_comment_user_data
    
    except Exception as e:
        print(f"Error at like_comment {str(e)}")
        return f"Error: {str(e)}"


def get_user_comment_list(page, per_page):

    try:
        comment_list = []
        sub_comment = {}
        users = Users.query.paginate(page=page, per_page=per_page)
        like_comment_user_data = get_like_comment_user(page, per_page)
        if isinstance(like_comment_user_data, tuple):
            if like_comment_user_data == "invalid json data":
                return like_comment_user_data
            elif like_comment_user_data == "like_comment_id not found":
                return like_comment_user_data
        like_comment_user_data
        for user in users:
            for comment in user.comments:
                # using backref go to blog_comment table
                # blog = comment.blog_relation
                data = {
                    "comment": comment.text,
                    "comment_id": comment.id,
                    "username": user.username,
                    "likes": comment.id,
                }
                if comment.parent_comment_id == None:
                    comment_list.append(data)
                else:
                    parent_id = comment.parent_comment_id
                    if parent_id not in sub_comment:
                        sub_comment[parent_id] = []
                    sub_comment[parent_id].append(data)
        for comment in comment_list:
            comment_id = comment["comment_id"]
            id = comment["comment_id"]
            comment["likes"] = like_comment_user_data.get(id, [])
            comment["replies"] = sub_comment.get(comment_id, [])
        # # finding the sub-users who comment on blog
        for comment in comment_list:
            for reply in comment["replies"]:
                reply_id = reply["comment_id"]
                id = reply["comment_id"]
                reply["likes"] = like_comment_user_data.get(id, [])
                reply["replies"] = sub_comment.get(reply_id, [])
                for sub_reply in reply["replies"]:
                    sub_reply_id = sub_reply["comment_id"]
                    id = sub_reply["comment_id"]
                    sub_reply["likes"] = like_comment_user_data.get(id, [])
                    sub_reply["replies"] = sub_comment.get(sub_reply_id, [])
                    for sub_sub_reply in sub_reply["replies"]:
                        sub_sub_reply_id = sub_sub_reply["comment_id"]
                        id = sub_sub_reply["comment_id"]
                        sub_sub_reply["likes"] = like_comment_user_data.get(id, [])
                        sub_sub_reply["replies"] = sub_comment.get(sub_sub_reply_id, [])
        return comment_list
    except Exception as e:
        print(f"Error at get_user_comment {str(e)}")
        return f"Error: {str(e)}"
