import os

from django.db import connection
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



def open_connection():
    with psycopg2.connect(DATABASE_URL) as conn:
        return conn


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    connection = open_connection()
    urls = urls_repo.get_all_urls(connection)
    return render_template('urls.html', urls=urls)


@app.post('/new_url')
def add_url():
    url = request.form.get('url')
    return {1: 2}