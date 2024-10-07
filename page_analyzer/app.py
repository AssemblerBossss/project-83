from flask import Flask
from flask import (
    render_template,
    redirect,
    request,
)
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/new_url')
def add_url():
    url = request.form.get('url')
    return {1: 2}