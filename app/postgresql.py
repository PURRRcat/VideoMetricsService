import psycopg2
import time

class PostgresAPI:
    def __init__(self, dbname="database", user="user", password="strong_password", host="db", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cur = None

    def create_table(self, table_name):
        self.cur.execute(f"""   
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                server VARCHAR(100),
                cost INTEGER
            );
        """)
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
            except:
                print("faile")
                time.sleep(5)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cur:
            self.cur.close()
        if self.connection:
            self.connection.close()
        print("Соединение с базой данных закрыто.")


with PostgresAPI() as db:
    db.create_table("videos")
