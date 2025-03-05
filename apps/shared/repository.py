from django.db import connection
from datetime import datetime, timedelta

class ItemRepository:

    def create_item(self, data: dict) -> int:
        insert_sql = """
        INSERT INTO items
        (user_id, group_id, item_name, pickup_place, return_place, item_description, status,
        quantity, caution, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        RETURNING item_id
        """

        params = [
            data["user_id"],
            data["group_id"],
            data["item_name"],
            data.get("pickup_place", ""),
            data.get("return_place", ""),
            data.get("item_description", ""),
            data.get("status", 0),
            data.get("quantity", 1),
            data.get("caution", ""),
        ]

        with connection.cursor() as cursor:
            cursor.execute(insert_sql, params)
            row = cursor.fetchone()
            new_id = row[0]
        return new_id
    
    def create_item_image(self, item_id: int, image_url: str):
        image_url = 'https://kr.object.ncloudstorage.com/weshare/groups/C.JPG' # s3 업로드 기능 추가되면 삭제
        insert_sql = """
        INSERT INTO item_images (item_id, image_url, created_at)
        VALUES (%s, %s, NOW())
        """

        with connection.cursor() as cursor:
            cursor.execute(insert_sql, [item_id, image_url])

    def delete_item(self, item_ids: list) -> int:
        placeholders = ', '.join(['%s'] * len(item_ids))
        sql = f"DELETE FROM items WHERE item_id IN ({placeholders})"
        with connection.cursor() as cursor:
            cursor.execute(sql, item_ids)
            deleted_count = cursor.rowcount 
        return deleted_count

    def get_item_list(self, group_id: int, user_id: int, sorted: str, is_all: bool) -> list[dict]:
        if sorted.upper() not in ("ASC", "DESC"):
            raise ValueError("Invalid sort order. Use 'ASC' or 'DESC'")
        
        now = datetime.now()
        
        sql = f"""
        SELECT
            i.group_id,
            g.group_name,
            i.item_id,
            i.item_name,
            COALESCE(ARRAY_AGG(im.image_url) FILTER (WHERE im.image_url IS NOT NULL), ARRAY[]::TEXT[]) AS image_urls,
            i.quantity,
            i.created_at,
            COALESCE(
                MAX(
                    CASE 
                        WHEN rr.rental_start <= %s 
                        AND rr.rental_end >= %s
                        AND rr.rental_status != 3 THEN 
                            CASE 
                                WHEN rr.rental_status = 2 THEN 2  -- 픽업 완료, 반납 가능 상태
                                ELSE 1  -- 예약 완료, 픽업 가능 상태
                            END
                        ELSE 0 -- 예약 가능 상태
                    END
                ), 0
            ) AS status,
            CASE 
                WHEN EXISTS (
                    SELECT 1 FROM wishlists w WHERE w.user_id = %s AND w.item_id = i.item_id
                ) THEN 1 
                ELSE 0 
            END AS is_wishlist,
            i.user_id AS reservation_user_id,
            u.username AS reservation_user_name
        FROM items i
        JOIN groups_group g ON i.group_id = g.group_id
        JOIN groups_groupmember gm ON i.group_id = gm.group_id
        LEFT JOIN item_images im ON im.item_id = i.item_id
        LEFT JOIN auth_user u ON i.user_id = u.id
        LEFT JOIN rental_records rr 
            ON i.item_id = rr.item_id 
            AND rr.rental_end >= %s  -- 현재보다 미래의 예약만 고려
            AND rr.rental_status != 3 -- rental_status = 3인 것은 무시
        WHERE gm.user_id = %s
        """

        params = [now, now, user_id, now, user_id]
        
        if group_id != 0:
            sql += " AND i.group_id = %s"
            params.append(group_id)

        sql += f" GROUP BY i.item_id, i.group_id, g.group_name, i.item_name, i.quantity, i.created_at, i.user_id, u.username"
        sql += f" ORDER BY i.created_at {sorted}"
        
        if not is_all:
            sql += f" NULLS LAST LIMIT 6"

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

        result_list = [dict(zip(col_names, row)) for row in rows]
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
            COALESCE(ARRAY_AGG(im.image_url) FILTER (WHERE im.image_url IS NOT NULL), ARRAY[]::TEXT[]) AS image_urls,
            i.status,
            i.quantity,
            i.caution,
            i.created_at,
            COALESCE(
                JSONB_AGG(
                    JSONB_BUILD_OBJECT(
                        'rental_start', r.rental_start,
                        'rental_end', r.rental_end,
                        'username', u.username,
                        'profile_image', u.profile_image
                    ) ORDER BY r.rental_start
                ) FILTER (WHERE r.rental_status = 3),
                '[]'::JSONB
            ) AS rental_history
        FROM items i
        JOIN groups_group g ON i.group_id = g.group_id
        LEFT JOIN item_images im ON im.item_id = i.item_id
        JOIN users u ON i.user_id = u.id
        LEFT JOIN rental_records r ON i.item_id = r.item_id
        WHERE i.item_id = %s
        GROUP BY i.user_id, u.username, i.group_id, g.group_name, i.item_id, i.item_name, i.pickup_place, 
            i.return_place, i.item_description, i.status, i.quantity, i.caution, i.created_at
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [item_id])
            row = cursor.fetchone()
            if not row:
                return None
            col_names = [desc[0] for desc in cursor.description]

        return dict(zip(col_names, row))

    def get_available_times(self, item_id: int) -> list:
        now = datetime.now().replace(second=0, microsecond=0)
        if now.minute % 30 != 0:
            now += timedelta(minutes=30 - now.minute % 30)
            
        end_time = now + timedelta(days=7)
        time_slots = []
        
        temp_time = now
        while temp_time <= end_time:
            time_slots.append(temp_time.strftime("%Y-%m-%d %H:%M"))
            temp_time += timedelta(minutes=30)

        sql = """
        SELECT rental_start, rental_end
        FROM rental_records
        WHERE item_id = %s
        AND rental_status != 3
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [item_id])
            reserved_times = cursor.fetchall()

        for rental_start, rental_end in reserved_times:
            rental_start = rental_start.strftime("%Y-%m-%d %H:%M")
            rental_end = rental_end.strftime("%Y-%m-%d %H:%M")
            time_slots = [t for t in time_slots if not (rental_start <= t < rental_end)]

        return time_slots

    def get_available_time_ranges(self, item_id: int) -> list:
        now = datetime.now().replace(second=0, microsecond=0)
        if now.minute % 30 != 0:
            now += timedelta(minutes=30 - now.minute % 30)

        end_time = now + timedelta(days=7)

        time_slots = []
        temp_time = now
        while temp_time <= end_time:
            time_slots.append(temp_time)
            temp_time += timedelta(minutes=30)

        sql = """
        SELECT rental_start, rental_end
        FROM rental_records
        WHERE item_id = %s
        AND rental_status != 3
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [item_id])
            reserved_times = cursor.fetchall()

        for rental_start, rental_end in reserved_times:
            rental_start = rental_start.replace(second=0, microsecond=0)
            rental_end = rental_end.replace(second=0, microsecond=0)
            time_slots = [t for t in time_slots if not (rental_start <= t < rental_end)]

        available_ranges = []
        if not time_slots:
            return available_ranges

        start_time = time_slots[0]
        for i in range(1, len(time_slots)):
            if (time_slots[i] - time_slots[i - 1]) != timedelta(minutes=30):
                available_ranges.append({
                    "start": start_time.strftime("%Y-%m-%d %H:%M"),
                    "end": time_slots[i - 1].strftime("%Y-%m-%d %H:%M")
                })
                start_time = time_slots[i]

        available_ranges.append({
            "start": start_time.strftime("%Y-%m-%d %H:%M"),
            "end": time_slots[-1].strftime("%Y-%m-%d %H:%M")
        })

        return available_ranges

    def reserve_item(self, user_id: int, item_id: int, rental_start: str, rental_end: str):
        sql = """
        INSERT INTO rental_records
        (user_id, item_id, rental_start, rental_end, actual_return, rental_status, pickup_image, return_image, created_at)
        VALUES (%s, %s, %s, %s, null, 1, null, null, NOW());
        """
        params = [user_id, item_id, rental_start, rental_end]
        with connection.cursor() as cursor:
            cursor.execute(sql, params)

    def get_reserved_items(self, group_id: int, user_id: int, sorted: str) -> list[dict]:
        if sorted.upper() not in ("ASC", "DESC"):
            raise ValueError("Invalid sort order. Use 'ASC' or 'DESC'")

        sql = """
        SELECT
            i.group_id,
            g.group_name,
            i.item_id,
            i.item_name,
            COALESCE(ARRAY_AGG(im.image_url) FILTER (WHERE im.image_url IS NOT NULL), ARRAY[]::TEXT[]) AS image_urls,
            i.quantity,
            i.created_at,
            i.status,
            MAX(r.rental_start) AS rental_start,
            MAX(r.rental_end) AS rental_end,
            CASE 
                WHEN EXISTS (
                    SELECT 1 FROM wishlists w WHERE w.user_id = %s AND w.item_id = i.item_id
                ) THEN 1 
                ELSE 0 
            END AS is_wishlist,
            i.user_id AS reservation_user_id,
            u.username AS reservation_user_name
        FROM rental_records r
        JOIN items i ON r.item_id = i.item_id
        JOIN groups_group g ON i.group_id = g.group_id
        LEFT JOIN item_images im ON im.item_id = i.item_id
        LEFT JOIN users u ON i.user_id = u.id
        WHERE r.user_id = %s
        AND r.rental_status < 3
        """

        params = [user_id, user_id]
        if group_id != 0:
            sql += " AND i.group_id = %s"
            params.append(group_id)
            
        sql += f" GROUP BY i.item_id, i.group_id, g.group_name, i.item_name, i.quantity, i.created_at, i.status, i.user_id, u.username, r.rental_start"
        sql += f" ORDER BY r.rental_start DESC, i.created_at {sorted} NULLS LAST LIMIT 6"
        
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

        return [dict(zip(col_names, row)) for row in rows]
    
    
    def pickup_item(self, user_id: int, item_id: int, pickup_time: str, pickup_image: str) -> dict | None:
        sql = """
        update rental_records 
        set rental_status = 2, 
        pickup_image = %s,
        pickup_time = %s
        where item_id = %s
        and rental_status = 1
        and user_id = %s;
        UPDATE items SET status = 2 where item_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [pickup_image, pickup_time, item_id, user_id, item_id])
        return {
            "user_id": user_id,
            "item_id": item_id,
            "rental_start": pickup_time, 
            "rental_end": str(pickup_image), 
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
            COALESCE(ARRAY_AGG(im.image_url) FILTER (WHERE im.image_url IS NOT NULL), ARRAY[]::TEXT[]) AS image_urls,
            i.status
            i.quantity,
            i.caution,
            r.rental_start,
            r.rental_end
        FROM rental_records r
        JOIN items i ON r.item_id = i.item_id
        JOIN groups g ON i.group_id = g.group_id
        LEFT JOIN item_images im ON im.item_id = i.item_id
        WHERE r.user_id = %s
        AND r.rental_status = '2'
        GROUP BY r.user_id, i.group_id, g.group_name, i.item_id, i.item_name, i.item_description, i.status, i.quantity, i.caution, r.rental_start, r.rental_end
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
        sql = """
        update rental_records 
        set rental_status = 3, 
        return_image = %s,
        return_time = %s
        where item_id = %s
        and rental_status = 2
        and user_id = %s;
        UPDATE items SET status = 0 where item_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [return_image, return_time, item_id, user_id, item_id])
        return {
            "user_id": user_id,
            "item_id": item_id,
            "rental_start": return_time, 
            "rental_end": str(return_image), 
        }
    
class WishlistRepository:
    def add_wishlist(self, user_id: int, item_id: int) -> bool:
        check_sql = "SELECT COUNT(*) FROM wishlists WHERE user_id = %s AND item_id = %s"
        insert_sql = "INSERT INTO wishlists (user_id, item_id) VALUES (%s, %s)"

        with connection.cursor() as cursor:
            cursor.execute(check_sql, [user_id, item_id])
            is_existing = cursor.fetchone()[0]

            if is_existing:
                return False
            
            cursor.execute(insert_sql, [user_id, item_id])
            return True

    def remove_wishlist(self, user_id: int, item_id: int) -> bool:
        check_sql = "SELECT COUNT(*) FROM wishlists WHERE user_id = %s AND item_id = %s"
        delete_sql = "DELETE FROM wishlists WHERE user_id = %s AND item_id = %s"

        with connection.cursor() as cursor:
            cursor.execute(check_sql, [user_id, item_id])
            is_existing = cursor.fetchone()[0]

            if not is_existing:
                return False

            cursor.execute(delete_sql, [user_id, item_id])
            return True