from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # sql operations
from sqlalchemy import Table, Column, ForeignKey, or_, and_
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta

app = Flask(__name__)
cors = CORS(app)

APP_URL = "http://localhost:5001"

app.secret_key = "UElvxzayo733SL2e73qd4MPezy4Dds"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://agilizamed:123405@localhost/agilizamed?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

