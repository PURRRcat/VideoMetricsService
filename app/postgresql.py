import psycopg2
import time

class PostgresAPI:
    def __init__(self, dbname="database", user="user", password="strong_password", host="postgres_container", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cur = None

    def insert(self):
        self.cur.execute(f"""   
                    INSERT INTO videos
                    DEFAULT VALUES
                    RETURNING id, status;
                    """)
        video_id, status = self.cur.fetchone()
        self.connection.commit()
        return video_id, status

    def insert_status(self, status, video_id):
        self.cur.execute(f"""   
                    UPDATE videos
                    SET status = %s
                    WHERE id = %s;;
                    """, (status, video_id))
        self.connection.commit()

    def insert_values(self, video_size, encoding_time, decoding_time, video_id):
        self.cur.execute(f"""   
            UPDATE videos 
            SET video_size = %s, encoding_time = %s, decoding_time = %s
            WHERE id = %s;;
            """, (video_size, encoding_time, decoding_time, video_id))
        self.connection.commit()

    def get_id(self, video_id):
        self.cur.execute("""
            SELECT video_size, encoding_time, decoding_time
            FROM videos
            WHERE id = %s;
            """, (video_id,))
        return self.cur.fetchone()

    def get_status(self, video_id):
        self.cur.execute("""
                    SELECT status
                    FROM videos
                    WHERE id = %s;
                    """, (video_id,))
        return self.cur.fetchone()[0]

    def delete_video(self, video_id):
        self.cur.execute("""
            DELETE FROM videos
            WHERE id = %s;
        """, (video_id,))
        self.connection.commit()

    def __enter__(self):
        while True:
            try:
                self.connection = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                self.cur = self.connection.cursor()
                return self
            except Exception as e:
                print(e)
                time.sleep(5)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cur:
            self.cur.close()
        if self.connection:
            self.connection.close()
        print("Соединение с базой данных закрыто.")


