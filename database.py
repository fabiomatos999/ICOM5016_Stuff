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
            self.createLoginTable()
            self.createChainsTable()
            self.createClientTable()
            self.createHotelTable()
            self.createRoomUnavailableTable()

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

    def createLoginTable(self):
        """Create Login table if it does not already exist."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Login (
            lid SERIAL PRIMARY KEY,
            eid INTEGER NOT NULL,
            username VARCHAR NOT NULL,
            password VARCHAR NOT NULL);""")
        self.conn.commit()

    def createChainsTable(self):
        """Create Chains table if it does not already exist."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Chains (
            chid SERIAL PRIMARY KEY,
            cname VARCHAR NOT NULL,
            springmkup float NOT NULL,
            summermkup float NOT NULL,
            fallmkup float NOT NULL,
            wintermkup float NOT NULL);""")
        self.conn.commit()

    def __del__(self):
        """Close database connection when object is destroyed."""
        self.conn.close()

    def createClientTable(self):
        """Create Client table if it does not already exist."""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Client (clid SERIAL PRIMARY KEY,
       fname VARCHAR NOT NULL,lname VARCHAR NOT NULL,
       age INTEGER NOT NULL,memberyear INTEGER NOT NULL);""")
        self.conn.commit()

    def createHotelTable(self):
        """Create Hotel table if it does not already exist."""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Hotel (hid SERIAL PRIMARY KEY,
            chid INTEGER NOT NULL,
            hname VARCHAR NOT NULL,hcity VARCHAR NOT NULL);""")
        self.conn.commit()

    def createRoomUnavailableTable(self):
        """Create RoomUnavailable table if it does not already exist."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS RoomUnavailable
            (ruid SERIAL PRIMARY KEY,
            rid INTEGER NOT NULL,startdate
            DATE NOT NULL,enddate DATE NOT NULL);""")
        self.conn.commit()
