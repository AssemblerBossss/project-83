import os
from dotenv import load_dotenv
import psycopg2
from .url_repo import (
    add_new_url_to_db,
    get_all_urls,
    add_url_check,
    get_latest_url_check,
    get_url_checks_by_id,
    get_url_name_by_id,
    get_url_id_if_exists,
)

from flask import (
    Flask,
    render_template,
    redirect,
    request, flash,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    urls = get_all_urls()
    return render_template('urls.html', urls=urls)


@app.post('/new_url')
def add_url():
    url = request.form.get('url')
    existing_url = get_url_id_if_exists(url)
    if existing_url:
        flash('Страница уже существует', 'alert-info')
        return redirect('/')
    else:
        added_url_id = add_new_url_to_db(url)
        flash('Страница успешно добавлена', 'alert-success')
        return redirect('/')


@app.get('/urls/<id>')
def show_url_info(id):
    return {1:1}
