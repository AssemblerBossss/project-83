import os
import requests
from http import HTTPStatus
from dotenv import load_dotenv
from validators import ValidationError
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash,
    url_for,
    Response,
)

from .parser import get_seo_information
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


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index() -> str:
    """
    Отображает главную страницу приложения.

    Returns:
        str: HTML-шаблон главной страницы.
    """
    return render_template('index.html')


@app.get('/urls')
def get_urls() -> str:
    """
    Отображает страницу со списком всех URL-адресов и их последних проверок.

    Returns:
        str: HTML-шаблон страницы со списком URL-адресов и их последних проверок.
    """

    urls = get_all_urls()
    checks = get_latest_url_check()
    checks_dict = {check.url_id: check for check in checks}
    return render_template('urls.html', urls=urls, checks=checks_dict)


@app.post('/new_url')
def add_url() -> tuple[str, int] | Response:
    """
    Обрабатывает POST-запрос для добавления нового URL-адреса.
    """

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
    except ValidationError:
        flash('Ошибка валидации URL', 'alert-danger')
        return render_template('index.html'), 422


@app.get('/urls/<id>')
def show_url_info(id):
    """
    Отображает страницу с информацией о конкретном URL-адресе и его проверках.

    Args:
        id (int): Идентификатор URL-адреса.

    Returns:
        str: HTML-шаблон страницы с информацией о URL-адресе и его проверках.
    """

    url_info = get_url_info_by_id(id)
    url_check = get_url_checks_by_id(id)
    return render_template('url.html', url_info=url_info, checks=url_check)


# noinspection PyUnreachableCode
@app.post('/urls/<id>/checks')
def check_url(id):
    url_name = get_url_name_by_id(id)
    try:
        responce = requests.get(url_name)
        status_code = responce.status_code
        if status_code == HTTPStatus.OK:
            site_data =  get_seo_information(responce.text)
            h1, title, description = site_data.get('h1'), \
                 site_data.get('title'), site_data.get('description')
            add_url_check(id, status_code, h1, title, description)
            flash('Страница успешно проверена', 'alert-success')
        else:
            flash('Произошла ошибка при проверке', 'alert-danger')
    except request.exception.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
    return redirect(url_for('show_url_info', id=id))
