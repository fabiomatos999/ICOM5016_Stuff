"""Database initialization and connection module.

This module was developed for the term project - Hotel Analytics Systems for
CIIC4060/ICOM 5016.
"""
import psycopg2


class DatabaseConnection:
    """Create database tables and connect to database."""

    def __init__(self, DB_NAME: str, DB_USER: str, DB_PASS: str, DB_HOST: str,
                 DB_PORT: str):
        """Create DatabaseConnection object and tables if they do not exist."""
        with psycopg2.connect(database=DB_NAME,
                              user=DB_USER,
                              password=DB_PASS,
                              host=DB_HOST,
                              port=DB_PORT) as conn:
            self.conn = conn
            self.cursor = conn.cursor()
            self.createRoomTable()
            self.createReserveTable()

    def createRoomTable(self):
        """Create Room table if it does not already exist."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Room (rid SERIAL,
                hid INTEGER NOT NULL, rdid INTEGER NOT NULL,
                rprice REAL NOT NULL);""")
        self.conn.commit()

    def createReserveTable(self):
        """Create Reserve table if it does not already exist."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Reserve (reid SERIAL,
            ruid INTEGER NOT NULL,
            clid INTEGER NOT NULL,
            total_cost REAL NOT NULL,
            payment TEXT,
            guests INTEGER NOT NULL);""")
        self.conn.commit()

    def __del__(self):
        """Close database connection when object is destroyed."""
        self.conn.close()
