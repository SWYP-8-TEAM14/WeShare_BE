from django.db import connection


class ItemRepository:

    def create_item(self, data: dict) -> int:
        insert_sql = """
        INSERT INTO items
        (user_id, group_id, item_name, pickup_place, return_place, item_description, item_image, status,
         quantity, caution, created_at, deleted_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING item_id
        """

        params = [
            data["user_id"],
            data["group_id"],
            data["item_name"],
            data.get("pickup_place", ""),
            data.get("return_place", ""),
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
            row = cursor.fetchone()
            new_id = row[0]
        return new_id

    def delete_item(self, item_id: int) -> int:
        sql = "DELETE FROM items WHERE item_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, [item_id])
            deleted_count = cursor.rowcount 
        return deleted_count

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
        FROM items i
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

    def get_item_detail(self, item_id: int) -> dict | None:
        sql = """
        SELECT
            i.user_id,
			u.username,
            i.group_id,
            g.group_name,
            i.item_id,
            i.item_name,
			i.pickup_place,
			i.return_place,
            i.item_description,
            i.item_image,
            i.status,
            i.quantity,
            i.caution,
            i.created_at
        FROM items i
        JOIN groups_group g ON i.group_id = g.group_id
		JOIN auth_user u ON i.user_id = u.id
        WHERE i.item_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [item_id])
            row = cursor.fetchone()
            if not row:
                return None
            col_names = [desc[0] for desc in cursor.description]

        return dict(zip(col_names, row))
    
    def reserve_item(self, user_id: int, item_id: int, start_time: str, end_time: str):
        sql = """
        INSERT INTO reservations
        (user_id, item_id, start_time, end_time, reservation_date, status, created_at)
        VALUES (%s, %s, %s, %s, NOW(), 'RESERVED', NOW())
        """
        params = [user_id, item_id, start_time, end_time]
        with connection.cursor() as cursor:
            cursor.execute(sql, params)

    def get_reserved_items(self, user_id: int) -> list[dict]:
        sql = """
        SELECT
            r.reservation_id,
            r.user_id,
            r.item_id,
            r.start_time,
            r.end_time,
            r.status,
            r.created_at AS reservation_created,
            i.item_name,
            i.item_description,
            i.item_image
        FROM reservations r
        JOIN items i ON r.item_id = i.item_id
        WHERE r.user_id = %s
          AND r.status = 'RESERVED'
        ORDER BY r.created_at DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [user_id])
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

        result = []
        for row in rows:
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)
        return result
    
    def pickup_item(self, user_id: int, item_id: int, pickup_time: str, image: str) -> dict | None:
        find_sql = """
        SELECT start_time, end_time
        FROM reservations
        WHERE user_id = %s
          AND item_id = %s
          AND status = 'RESERVED'
        ORDER BY created_at DESC
        LIMIT 1
        """
        with connection.cursor() as cursor:
            cursor.execute(find_sql, [user_id, item_id])
            row = cursor.fetchone()
        if not row:
            return None 
        
        start_time, end_time = row 

        insert_sql = """
        INSERT INTO rental_records
        (user_id, item_id, rental_start, rental_end, rental_status, pickup_image, created_at)
        VALUES (%s, %s, %s, %s, 'ON_RENT', %s, NOW())
        RETURNING rental_id
        """
        params = [user_id, item_id, pickup_time, end_time, image]
        with connection.cursor() as cursor:
            cursor.execute(insert_sql, params)
        return {
            "user_id": user_id,
            "item_id": item_id,
            "start_time": pickup_time, 
            "end_time": str(end_time), 
        }
    

    def get_returnable_items(self, user_id: int) -> list[dict]:
        sql = """
        SELECT
            r.user_id,
            i.group_id,
            g.group_name,
            i.item_id,
            i.item_name,
            i.item_description,
            i.item_image,
            i.status AS item_status,   -- items 테이블의 status
            i.quantity,
            i.caution,
            r.rental_start AS start_time,
            r.rental_end   AS end_time
        FROM rental_records r
        JOIN items i ON r.item_id = i.item_id
        JOIN groups g ON i.group_id = g.group_id
        WHERE r.user_id = %s
          AND r.rental_status = 'ON_RENT'
        ORDER BY r.created_at DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [user_id])
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

        result = []
        for row in rows:
            result.append(dict(zip(col_names, row)))
        return result
    
    def return_item(self, user_id: int, item_id: int, return_time: str, return_image: str) -> dict | None:
        find_sql = """
        SELECT rental_id, rental_start, rental_end
        FROM rental_records
        WHERE user_id = %s
          AND item_id = %s
          AND rental_status = 'ON_RENT'
        ORDER BY created_at DESC
        LIMIT 1
        """
        with connection.cursor() as cursor:
            cursor.execute(find_sql, [user_id, item_id])
            row = cursor.fetchone()
        if not row:
            return None 

        rental_id, rental_start, rental_end = row

        update_sql = """
        UPDATE rental_records
        SET actual_return = %s,
            return_image  = %s,
            rental_status = 'RETURNED'
        WHERE rental_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(update_sql, [return_time, return_image, rental_id])

        return {
            "user_id": user_id,
            "item_id": item_id,
            "start_time": str(rental_start),
            "end_time": str(rental_end),
        }