import os
from dotenv import load_dotenv
import psycopg2


from flask import (
    Flask,
    render_template,
    redirect,
    request,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def open_connection():
    with psycopg2.connect(DATABASE_URL) as conn:
        return conn
# def open_connection():
#     conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),)
#     return conn

@app.get('/')
def index():
    return render_template('index.html')


# @app.get('/urls')
# def get_urls():
#     conn =

@app.post('/new_url')
def add_url():
    url = request.form.get('url')
    return {1: 2}