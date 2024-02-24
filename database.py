import psycopg2

DB_NAME = "db"
DB_USER = "uwu"
DB_PASS = "uwu"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"


class DatabaseConnection:

    def __init__(self):
        with psycopg2.connect(database=DB_NAME,
                              user=DB_USER,
                              password=DB_PASS,
                              host=DB_HOST,
                              port=DB_PORT) as conn:
            self.conn = conn
            self.cursor = conn.cursor()
            self.create_rooms_table()
            self.create_reserve_table()

    def create_rooms_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Room (rid SERIAL,
                hid INTEGER NOT NULL, rdid INTEGER NOT NULL,
                rprice REAL NOT NULL);""")
        self.conn.commit()

    def create_reserve_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Reserve (reid SERIAL,
            ruid INTEGER NOT NULL,
            clid INTEGER NOT NULL,
            total_cost REAL NOT NULL,
            payment TEXT,
            guests INTEGER NOT NULL);""")
        self.conn.commit()

    def __del__(self):
        self.conn.close()
