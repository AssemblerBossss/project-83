import os
from dotenv import load_dotenv
import psycopg2
from .validator import normalize_url, is_valid_url
from .url_repo import (
    add_new_url_to_db,
    get_all_urls,
    add_url_check,
    get_latest_url_check,
    get_url_checks_by_id,
    get_url_name_by_id,
    get_url_id_if_exists,
    get_url_info_by_id
)

from flask import (
    Flask,
    render_template,
    redirect,
    request, flash, url_for,
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
    try:
        if is_valid_url(url):
            normalized_url = normalize_url(url)
            existing_url: int = get_url_id_if_exists(normalized_url)
            if existing_url:
                flash('Url already exists')
                return redirect(url_for('show_url_info', id=existing_url))
            else:
                added_url_id = add_new_url_to_db(normalized_url)
                flash('Url added', 'alert-success')
                return redirect(url_for('show_url_info', id=added_url_id))

        else:
            flash('Invalid URL', 'alert-danger')
            return render_template('index.html'), 422
    except Exception as e:
        flash('Ошибка валидации URL', 'alert-danger')
        return render_template('index.html'), 422


@app.get('/urls/<id>')
def show_url_info(id):
    url_info = get_url_info_by_id(id)
    url_check = get_url_checks_by_id(id)
    return render_template('url.html', url_info=url_info, check=url_check)
