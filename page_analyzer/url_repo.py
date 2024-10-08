from datetime import datetime
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
    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                '''SELECT * FROM urls WHERE name = %s''', (url,)
            )
            result = cursor.fetchone()
            return result.id if result else None


def get_all_urls():
    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                '''SELECT * FROM urls ORDER BY created_at DESC'''
            )
            return cursor.fetchall()


def add_url(url) -> int:
    current_date = datetime.now().strftime('%Y-%m-%d')
    with get_db_connection() as connection:
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                '''INSERT INTO urls (name, created_at)
                 VALUES (%s, %s, %s) RETURNING id''', (url, current_date)
            )
            new_id = cursor.fetchone()[0]
            connection.commit()
            return new_id


def get_url_by_name(connection, name):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            '''SELECT * FROM urls 1 WHERE name = %s''', (name,)
        )
        return cursor.fetchone()

