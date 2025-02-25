from django.db import connection


class ItemRepository:

    def create_item(self, data: dict) -> int:
        insert_sql = """
        INSERT INTO shared_item
        (user_id, group_id, item_name, item_description, item_image, status,
         quantity, caution, created_at, deleted_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING item_id
        """

        params = [
            data["user_id"],
            data["group_id"],
            data["item_name"],
            data.get("item_description", ""),
            data.get("item_image", ""),
            data.get("status", 1),
            data.get("quantity", 1),
            data.get("caution", ""),
            data.get("created_at", None),
            data.get("deleted_at", None),
        ]

        with connection.cursor() as cursor:
            cursor.execute(insert_sql, params)
            row = cursor.fetchone()  # (new_id,)
            new_id = row[0]
        return new_id

    def get_item_list(self, user_id: int) -> list[dict]:
        sql = """
        SELECT
            i.group_id,
            g.group_name,
            i.item_id,
            i.item_name,
            i.item_image,
            i.quantity,
            i.created_at,
            i.status,
            0   AS is_wishlist,
            NULL AS reservation_user_id,
            NULL AS reservation_user_name
        FROM shared_item i
        JOIN groups_group g ON i.group_id = g.group_id
        WHERE i.user_id = %s
        ORDER BY i.created_at DESC NULLS LAST
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [user_id])
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

        result_list = []
        for row in rows:
            row_dict = dict(zip(col_names, row))
            result_list.append(row_dict)
        return result_list

    def get_item_detail(self, user_id: int, item_id: int) -> dict | None:
        sql = """
        SELECT
            i.user_id,
            i.group_id,
            g.group_name,
            i.item_id,
            i.item_name,
            i.item_description,
            i.item_image,
            i.status,
            i.quantity,
            i.caution,
            i.created_at
        FROM shared_item i
        JOIN groups_group g ON i.group_id = g.group_id
        WHERE i.user_id = %s
          AND i.item_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [user_id, item_id])
            row = cursor.fetchone()
            if not row:
                return None
            col_names = [desc[0] for desc in cursor.description]

        return dict(zip(col_names, row))