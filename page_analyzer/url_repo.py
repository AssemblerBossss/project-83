from datetime import date
from psycopg2.extras import NamedTupleCursor



def add_url(connection, url):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            '''INSERT INTO urls (name, created_at)
             VALUES (%s %s) RETURNING id;''', (url, date.today())
        )
        id = cursor.fetchone().id
        return id


def get_url_by_id(connection, id):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            '''SELECT * FROM urls 1 WHERE id = %s''', (id,)
        )
        return cursor.fetchone()

def get_url_by_name(connection, name):
    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            '''SELECT * FROM urls 1 WHERE name = %s''', (name,)
        )
        return cursor.fetchone()

