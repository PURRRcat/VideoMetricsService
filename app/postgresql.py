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

    def insert(self, video_size, encoding_time, decoding_time):
        self.cur.execute(f"""   
            INSERT INTO videos (video_size, encoding_time, decoding_time)
            VALUES (%s, %s, %s)
            RETURNING id;
            """, (video_size, encoding_time, decoding_time))
        video_id = self.cur.fetchone()[0]
        self.connection.commit()
        return video_id

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


with PostgresAPI() as db:
    db.insert("1", "1", "1")
