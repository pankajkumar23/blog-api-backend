from flask import Flask
from models.db import db
from routes.main_router import main_router
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.json.sort_keys = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return{"message":"server is running"}


app.register_blueprint(main_router)

if __name__ =='__main__':
    app.run(debug=True)