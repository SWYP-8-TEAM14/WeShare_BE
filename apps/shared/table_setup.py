from django.db import connection

def create_item_table():
    """
    PostgreSQL에 shared_item 테이블을 Raw SQL로 생성.
    필요하다면 수동으로 DB 콘솔(psql 등)에서 실행해도 됩니다.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS shared_item (
        item_id       SERIAL PRIMARY KEY,
        user_id       INTEGER NOT NULL,
        group_id      INTEGER NOT NULL,
        item_name     VARCHAR(255) NOT NULL,
        item_description TEXT,
        item_image    TEXT,
        status        INTEGER DEFAULT 1,
        quantity      INTEGER DEFAULT 1,
        caution       TEXT,
        created_at    TIMESTAMP,
        deleted_at    TIMESTAMP
    );
    """

    with connection.cursor() as cursor:
        cursor.execute(create_table_sql)
