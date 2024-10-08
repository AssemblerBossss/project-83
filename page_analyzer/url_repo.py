from datetime import datetime
from typing import NamedTuple, NoReturn
from psycopg2.extras import NamedTupleCursor
from contextlib import contextmanager
import os
import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL')


@contextmanager
def get_db_connection():
    """Контекстный менеджер для работы с базой данных."""
    connection = psycopg2.connect(DATABASE_URL)
    try:
        yield connection
    except Exception as e:
        connection.rollback()  # Отменить изменения при ошибке
        raise e
    finally:
        connection.close()


def get_url_id_if_exists(url):
    """
    Проверяет, существует ли заданный URL в базе данных, и возвращает его ID, если он существует.

    Args:
        url (str): URL для проверки.

    Returns:
        int or None: ID URL, если он существует, иначе None.
    """

    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                '''SELECT * FROM urls WHERE name = %s''', (url,)
            )
            result = cursor.fetchone()
            return result.id if result else None


def get_all_urls() ->list[NamedTuple]:
    """
    Возвращает все URL из базы данных, отсортированные по дате создания в порядке убывания.

    Returns:
        list: Список всех URL, отсортированных по дате создания в порядке убывания.
    """

    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                '''SELECT * FROM urls ORDER BY created_at DESC'''
            )
            return cursor.fetchall()


def add_new_url_to_db(url) -> int:
    """
    Добавляет новый URL в базу данных и возвращает его ID.

    Args:
        url (str): URL для добавления.

    Returns:
        int: ID нового URL.
    """

    current_date = datetime.now().strftime('%Y-%m-%d')
    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'INSERT INTO urls (name, created_at)\n'
                '                 VALUES (%s, %s, %s) RETURNING id', (url, current_date)
            )
            new_id: int = cursor.fetchone()[0]
            connection.commit()
            return new_id


def get_url_checks_by_id(url_id: int) -> list[NamedTuple]:
    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'SELECT * FROM url_checks WHERE url_id = %s\n'
                '                 ORDER BY created_at DESC, id DESC', (url_id,)
            )
            return cursor.fetchall()



def add_url_check(id, statis_code, h1, title, description) -> NoReturn:
    current_date = datetime.now().strftime('%Y-%m-%d')
    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                '''INSERT INTO url_checks (url_id, statis_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)''', (id, statis_code, h1, title, description, current_date)
            )
            connection.commit()



