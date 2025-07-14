from django.db import connection
from django.db import connection, DatabaseError

def execute_sql(query, params=None, fetchone=False):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()


def update(query, params):
    try:
        execute_sql(query, params)
        return True
    except DatabaseError as e:
        print(f"Erro no UPDATE: {e}")
        return False
