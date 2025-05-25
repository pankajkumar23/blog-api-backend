from flask import Flask,Blueprint
from routes.user_router import user_router

main_router = Blueprint("v1",__name__)
main_router.register_blueprint(user_router)