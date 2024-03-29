"""Data extraction module for csv, xlsx, sqlite and json files for Phase 1.

This module was developed for the term project - Hotel Analytics Systems for
CIIC4060/ICOM 5016. This module is exclusively for implementing the objectives
in phase 1 of the project.
"""
import sqlite3
from typing import List
from database import DatabaseConnection
from datetime import date

import pandas as pd


class ReserveTableData:
    """Data class used to represent the records inside of the reserve table.

    This class is used to represent the records inside of the reserve table
    of the reserve.db file given to us as a project resource.
    """

    def __init__(self, reid: int, ruid: int, clid: int, total_cost: float,
                 payment: str, guests: int):
        """Construct ReserveTableData.

        :param reid Auto incremented Primary Key for reserve table
        :param ruid Foreign key of the Room Unavailable table
        :param clid Foreign key of the Client table
        :param total_cost Total cost of a reservation
        :param payment Payment method
        :param guests Number of guests in a reservation

        Should only be used by the ReserveTableRawData class and not
        instantiated manually.
        """
        self.reid = reid
        self.ruid = ruid
        self.clid = clid
        self.total_cost = total_cost
        self.payment = payment
        self.guests = guests

    def __str__(self) -> str:
        """Return string representation of ReserveTableData."""
        s = (f"{self.reid}-{self.ruid}-{self.clid}-{self.total_cost}-"
             f"{self.payment}-{self.guests}")
        return s


class ReserveTableRawData:
    """Class to connect to reserve.db sqlite database and sanitize entries."""

    def __init__(self):
        """Connect to reserve.db database and sanitize input."""
        self.conn = sqlite3.connect("./Raw_Data/reserve.db")
        self.cursor = self.conn.cursor()
        raw_data = self.cursor.execute("""select reid,
        ruid, clid, total_cost, payment, guests from reserve;""").fetchall()
        raw_data: List[ReserveTableData] = list(
            map(lambda x: ReserveTableData(x[0], x[1], x[2], x[3], x[4], x[5]),
                raw_data))
        self.cleanData = self.sanitizeData(raw_data)

    def __del__(self):
        """Disconnect from reserve.db sqlite database."""
        self.conn.close()

    def sanitizeData(
            self, raw_data: List[ReserveTableData]) -> List[ReserveTableData]:
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            filter(
                lambda x: x.reid is not None and x.ruid is not None and x.clid
                is not None and x.total_cost is not None and x.payment is
                not None and x.payment != "" and x.guests is not None and x.
                guests >= 1, raw_data))

    def getCleanData(self) -> List[ReserveTableData]:
        """Get sanitized records from records.db sqlite database."""
        return self.cleanData

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Reserve table.

        Alters Reserve table by adding primary key constraint to reid.
        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO RESERVE (reid, ruid, clid,
                total_cost, payment, guests)
                VALUES (%s,%s,%s,%s,%s,%s)""",
                (record.reid, record.ruid, record.clid, record.total_cost,
                 record.payment, record.guests))
        conn.cursor.execute("""ALTER TABLE reserve ADD PRIMARY KEY (reid);""")
        conn.conn.commit()
        conn.cursor.execute("select max(reid) from reserve;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE reserve_reid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()


class RoomTableData:
    """Data class used to represent the records inside of the Room table.

    This class is used to represent the records inside of the reserve table
    of the rooms.db file given to us as a project resource.
    """

    def __init__(self, rid: int, hid: int, rdid: int, rprice: float):
        """Construct RoomTableData.

        :param rid Auto incremented Primary Key for Rooms table.
        :param hid Foreign Key for Hotel Table
        :param rdid Foreign Key for RoomDescription table
        :param rprice Price of the room

        Should only be used by the ReserveTableRawData class and not
        instantiated manually.
        """
        self.rid = rid
        self.hid = hid
        self.rdid = rdid
        self.rprice = rprice

    def __str__(self):
        """Return string representation of RoomTableData."""
        return f"{self.rid}-{self.hid}-{self.rdid}-{self.rprice}"


class RoomTableRawData:
    """Class to connect to rooms.db sqlite database and sanitize records."""

    def __init__(self):
        """Connect to rooms.db database and sanitize input."""
        self.conn = sqlite3.connect("./Raw_Data/rooms.db")
        self.cursor = self.conn.cursor()
        raw_data = self.cursor.execute("""
        select rid, hid, rdid, rprice from Room;""").fetchall()
        raw_data = list(
            map(lambda x: RoomTableData(x[0], x[1], x[2], x[3]), raw_data))
        self.cleanData = self.sanitizeData(raw_data)

    def __del__(self):
        """Disconnect from rooms.db sqlite database."""
        self.conn.close()

    def sanitizeData(self, raw_data: List[RoomTableData]):
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            filter(
                lambda x: x.rid is not None and x.hid is not None and x.rdid is
                not None and x.rprice is not None and x.rprice > 0, raw_data))

    def insertSanitizedRecords(self, conn: DatabaseConnection):
        """Insert clean data into the Room table.

        Alters Reserve table by adding primary key constraint to rid.
        Reset sequence to max after all data has been inserted.
        """
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO Room
                (rid, hid, rdid, rprice)
                VALUES (%s,%s,%s,%s)""",
                (record.rid, record.hid, record.rdid, record.rprice))
        conn.cursor.execute("""ALTER TABLE Room ADD PRIMARY KEY (rid);""")
        conn.conn.commit()
        conn.cursor.execute("select max(rid) from room;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE room_rid_seq
        restart with %s;""", (max, ))

    def getCleanData(self) -> List[ReserveTableData]:
        """Get sanitized records from rooms.db sqlite database."""
        return self.cleanData


class RoomDescriptionTableData:
    """Data class used to represent the records inside of the RoomDescription table."""

    def __init__(self, rdid: int, rname: str, rtype: str, capacity: int,
                 ishandicap: bool):
        """Construct RoomDescriptionData.

        :param rdid Auto incremented Primary Key for RoomDescription table.
        :param rname Name of the room.
        :param rtype Type of room.
        :param capacity Size of the room.
        :param ishandicap Checks if room is handicap.

        Should only be used by the RoomDescriptionTableRawData class and not
        instantiated manually.
        """
        self.rdid = rdid
        self.rname = rname
        self.rtype = rtype
        self.capacity = capacity
        self.ishandicap = ishandicap

    def __str__(self):
        """Return string representation of RoomDescriptionTableData."""
        return f"{self.rdid}-{self.rname}-{self.rtype}-{self.capacity}-{self.ishandicap}"


class RoomDescriptionTableRawData:
    """Class to open dataframe for Room Details JSON and sanitize records."""

    def __init__(self):
        """Read JSON File and sanitize input."""
        self.roomDescription_data = list()
        try:
            df = pd.read_json("Raw_Data/roomdetails.json")
            df = df.dropna()
            df['detailid'] = df['detailid'].astype(int)
            for index, row in df.iterrows():
                self.roomDescription_data.append(
                    RoomDescriptionTableData(row['detailid'], row['name'],
                                             row['type'], row['capacity'],
                                             bool(row['handicap'])))
        except Exception as e:
            print("Unable to read JSON", e)
            return None

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the RoomDescription table.
        Reset sequence to max after all data has been inserted."""
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO RoomDescription
                (rdid, rname, rtype, capacity, ishandicap)
                VALUES (%s,%s,%s,%s,%s)""",
                (record.rdid, record.rname, record.rtype, record.capacity,
                 record.ishandicap))
        conn.conn.commit()

        conn.cursor.execute("select max(rdid) from roomdescription;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE roomdescription_rdid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()

    def getCleanData(self) -> List[RoomDescriptionTableData]:
        return self.roomDescription_data


class LoginTableData:
    """Data class used to represent the records inside of the login table."""

    def __init__(self, lid: int, eid: int, username: str, password: str):
        """Construct LoginTableData.

        :param lid Auto incremented Primary Key for Login table.
        :param eid Foreign key for Employee table.
        :param username String representing the username.
        :param password String representing the password.

        Should only be used by the LoginTableRawData class and not
        instantiated manually.
        """
        self.lid = lid
        self.eid = eid
        self.username = username
        self.password = password

    def __str__(self):
        """Return string representation of LoginTableData."""
        return f"{self.lid}-{self.eid}-{self.username}-{self.password}"


class LoginTableRawData:
    """Class to open dataframe for Login XLSX and sanitize records."""

    def __init__(self):
        """Read Excel File and sanitize input."""
        self.login_data = list()
        try:
            df = pd.read_excel("Raw_Data/login.xlsx")
            df = df.dropna()
            df['lid'] = df['lid'].astype(int)
            for index, row in df.iterrows():
                self.login_data.append(
                    LoginTableData(row['lid'], row['employeeid'], row['user'],
                                   row['pass']))
        except Exception as e:
            print("Unable to read XLSX", e)
            return None

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Login table.
        Reset sequence to max after all data has been inserted."""
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO Login
                (lid, eid, username, password)
                VALUES (%s,%s,%s,%s)""",
                (record.lid, record.eid, record.username, record.password))
        conn.conn.commit()

        conn.cursor.execute("select max(lid) from login;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE login_lid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()

    def getCleanData(self) -> List[LoginTableData]:
        return self.login_data


class ChainsTableData:
    """Data class used to represent the records inside of the chains table."""

    def __init__(self, chid: int, cname: str, springmkup: float,
                 summermkup: float, fallmkup: float, wintermkup: float):
        """Construct ChainsTableData.

        :param chid Auto incremented Primary Key for Chains table.
        :param cname String representation of chain name.
        :param springmkup float representation of spring markup.
        :param summermkup float representation of summer markup.
        :param fallmkup float representation of fall markup.
        :param wintermkup float representation of winter markup.

        Should only be used by the ChainsTableRawData class and not
        instantiated manually.
        """
        self.chid = chid
        self.cname = cname
        self.springmkup = springmkup
        self.summermkup = summermkup
        self.fallmkup = fallmkup
        self.wintermkup = wintermkup

    def __str__(self):
        """Return string representation of ChainTableData."""
        return (f"{self.chid}-{self.cname}-{self.springmkup}-{self.summermkup}"
                f"-{self.fallmkup}-{self.wintermkup}")


class EmployeeTableData:
    """Data class used to represent the records inside of the Employee table."""

    def __init__(self, eid: int, hid: int, fname: str, lname: str,
                 position: str, salary: float):
        """Construct EmployeeData.

        :param eid Auto incremented Primary Key for Employee table.
        :param hid Foreign Key of the Hotel table.
        :param fname First name of the employee.
        :param lname Last name of the employee.
        :param position The work position of the employee.
        :param salary The money that the employee makes.

        Should only be used by the EmployeeTableRawData class and not
        instantiated manually.
        """
        self.eid = eid
        self.hid = hid
        self.fname = fname
        self.lname = lname
        self.position = position
        self.salary = salary

    def __str__(self):
        """Return string representation of EmployeeTableData."""
        return f"{self.eid}-{self.hid}-{self.fname}-{self.lname}-{self.position}-{self.salary}"


class EmployeeTableRawData:
    """Class to open dataframe for Employee JSON and sanitize records."""

    def __init__(self):
        """Read JSON File and sanitize input."""
        self.employee_data = list()
        try:
            df = pd.read_json("Raw_Data/employee.json")
            df = df.dropna()
            df['employee_id'] = df['employee_id'].astype(int)
            for index, row in df.iterrows():
                self.employee_data.append(
                    EmployeeTableData(row['employee_id'], row['hotel_id'],
                                      row['firstname'], row['lastname'],
                                      row['pos'], row['salary']))
        except Exception as e:
            print("Unable to read JSON", e)
            return None

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Employee table.
        Reset sequence to max after all data has been inserted."""
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO Employee
                (eid, hid, fname, lname, position, salary)
                VALUES (%s,%s,%s,%s,%s,%s)""",
                (record.eid, record.hid, record.fname, record.lname,
                 record.position, record.salary))
        conn.conn.commit()

        conn.cursor.execute("select max(eid) from employee;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE employee_eid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()

    def getCleanData(self) -> List[EmployeeTableData]:
        return self.employee_data


class ChainsTableRawData:
    """Class to open dataframe for Chains XLSX file and sanitize records."""

    def __init__(self):
        """Read Excel File and sanitize input."""
        self.chains_data = list()
        try:
            df = pd.read_excel("Raw_Data/chain.xlsx")
            df = df.dropna()
            df['id'] = df['id'].astype(int)
            for index, row in df.iterrows():
                self.chains_data.append(
                    ChainsTableData(row['id'], row['name'], row['spring'],
                                    row['summer'], row['fall'], row['winter']))
        except Exception as e:
            print("An error occurred:", e)
            return None

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Chains table.
        Reset sequence to max after all data has been inserted."""
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO Chains
                (chid, cname, springmkup, summermkup, fallmkup, wintermkup)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (record.chid, record.cname, record.springmkup,
                 record.summermkup, record.fallmkup, record.wintermkup))
        conn.conn.commit()

        conn.cursor.execute("select max(chid) from chains;")
        max = int(conn.cursor.fetchone()[0]) + 1
        conn.cursor.execute(
            """ALTER SEQUENCE chains_chid_seq
        restart with %s;""", (max, ))
        conn.conn.commit()

    def getCleanData(self) -> List[ChainsTableData]:
        return self.chains_data


class ClientTableData:
    """Class is used to represent the records inside the clients table."""

    def __init__(self, clid: int, fname: str, lname: str, age: int,
                 memberyear: int):
        """Create ClienTableData class.

        Args:
            clid (int): Serial primary key for Client table
            fname (str): Varchar of the client's first name
            lname (str): Varchar of the client's last name
            age (int): Integer of the client's age
            memberyear (int): Integer of Number of years client
            has been a member
        """
        self.clid = clid
        self.fname = fname
        self.lname = lname
        self.age = age
        self.memberyear = memberyear

    def __str__(self) -> str:
        """Return string representation of the ClientTableData Class."""
        s = (f"{self.clid}-{self.fname}-{self.lname}"
             f"-{self.age}-{self.memberyear}")
        return s


class ClientTableRawData:
    """Accesses the clients.csv file, sanitizes and inserts the entries."""

    def __init__(self):
        """Access the clients.csv file and sanitizes the input."""
        df = pd.read_csv('./Raw_Data/client.csv')
        df = df.dropna()
        raw_data = list()
        for index, row in df.iterrows():
            raw_data.append(
                ClientTableData(row['clid'], row[' fname'], row[' lastname'],
                                row[' age'], row[' memberyear']))
        self.cleanData = self.sanitizeData(raw_data)

    def sanitizeData(self,
                     raw_data: List[ClientTableData]) -> List[ClientTableData]:
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            # Filters out null values
            filter(
                lambda x: x.clid is not None and x.fname is not None and x.
                lname is not None and x.age is not None and x.memberyear is
                not None, raw_data))

    def getCleanData(self) -> List[ClientTableData]:
        """Get sanitized records from clients.csv file."""
        return self.cleanData

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Client table."""
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO CLIENT (clid, fname, lname, age, memberyear)
                VALUES(%s, %s, %s, %s, %s)""",
                (record.clid, record.fname, record.lname, record.age,
                 record.memberyear))
            conn.conn.commit()


class HotelTableData:
    """Class is used to represent the records inside the Hotel table."""

    def __init__(self, hid: int, chid: int, hname: str, hcity: str):
        """Create for JotelTableData class.

        Args:
            hid (int): Serial Primary key for Hotel table
            chid (int): Integer Foreign key from Chains Table
            hname (str): String of the hotel's name
            hcity (str): String of the city's name
        """
        self.hid = hid
        self.chid = chid
        self.hname = hname
        self.hcity = hcity

    def __str__(self) -> str:
        """Return string representation of the HotelTableData Class."""
        s = (f"{self.hid}-{self.chid}-{self.hname}-{self.hcity}")
        return s


class HotelTableRawData:
    """Class accesses the hotel.csv file, sanitizes and inserts the entries."""

    def __init__(self):
        """Access the clients.csv file and sanitizes the input."""
        df = pd.read_csv('./Raw_Data/hotel.csv')
        df = df.dropna()
        raw_data = list()
        for index, row in df.iterrows():
            raw_data.append(
                HotelTableData(row['hid'], row['chain'], row['name'],
                               row['city']))
        self.cleanData = self.sanitizeData(raw_data)

    def sanitizeData(self,
                     raw_data: List[HotelTableData]) -> List[HotelTableData]:
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            # Filters out null values
            filter(
                lambda x: x.hid is not None and x.chid is not None and x.hname
                is not None and x.hcity is not None, raw_data))

    def getCleanData(self) -> List[HotelTableData]:
        """Get sanitized records from hotel.csv file."""
        return self.cleanData

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the Hotel table."""
        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO HOTEL (hid, chid, hname, hcity)
                VALUES(%s, %s, %s, %s)""",
                (record.hid, record.chid, record.hname, record.hcity))
            conn.conn.commit()


class RoomUnavailableTableData:
    """Class to represent the records inside the RoomUnavailable table."""

    def __init__(self, ruid: int, rid: int, startdate: date, enddate: date):
        """Create for the RoomUnavailable class.

        Args:
            ruid (int): Serial Primary key for RoomUnavailable table
            rid (int): INteger Foreign key from Room table
            startdate (date): DATE, represents start date of room reservation
            enddate (date): DATE, represents end date of room reservation
        """
        self.ruid = ruid
        self.rid = rid
        self.startdate = startdate
        self.enddate = enddate

    def __str__(self) -> str:
        """Return string representation of RoomUnavailableTableData Class."""
        s = (f"{self.ruid}-{self.rid}-{self.startdate}-{self.enddate}")
        return s


class RoomUnavailableTableRawData:
    """Accesses room_unavailable.csv file, sanitize and inserts the entries."""

    def __init__(self):
        """Access the room_unavaible.csv file and sanitizes the input."""
        df = pd.read_csv('./Raw_Data/room_unavailable.csv')
        df = df.dropna()
        raw_data = list()
        for index, row in df.iterrows():
            raw_data.append(
                RoomUnavailableTableData(row['ruid'], row['rid'],
                                         row['start_date'], row['end_date']))
        self.cleanData = self.sanitizeData(raw_data)

    def sanitizeData(
        self, raw_data: List[RoomUnavailableTableData]
    ) -> List[RoomUnavailableTableData]:
        """Remove invalid (dirty) data for insertion into the database."""
        return list(
            # Filters out null values
            filter(
                lambda x: x.ruid is not None and x.rid is not None and x.
                startdate is not None and x.enddate is not None, raw_data))

    def getCleanData(self) -> List[RoomUnavailableTableData]:
        """Get sanitized records from room_unavailable.csv file."""
        return self.cleanData

    def insertSanitizedData(self, conn: DatabaseConnection):
        """Insert clean data into the RoomUnavailable table."""

        for record in self.getCleanData():
            conn.cursor.execute(
                """INSERT INTO ROOMUNAVAILABLE (ruid, rid, startdate, enddate)
                VALUES(%s, %s, %s, %s)""",
                (record.ruid, record.rid, record.startdate, record.enddate))
            conn.conn.commit()


if __name__ == "__main__":
    conn = DatabaseConnection("db", "uwu", "uwu", "127.0.0.1", "5432")
    loginData = LoginTableRawData()
    loginData.insertSanitizedData(conn)
    employeeData = EmployeeTableRawData()
    employeeData.insertSanitizedData(conn)
    hotelData = HotelTableRawData()
    hotelData.insertSanitizedData(conn)
    chainsData = ChainsTableRawData()
    chainsData.insertSanitizedData(conn)
    roomDescriptionData = RoomDescriptionTableRawData()
    roomDescriptionData.insertSanitizedData(conn)
    clientData = ClientTableRawData()
    clientData.insertSanitizedData(conn)
    roomData = RoomTableRawData()
    roomData.insertSanitizedRecords(conn)
    reserveData = ReserveTableRawData()
    reserveData.insertSanitizedData(conn)
    roomUnavailableData = RoomUnavailableTableRawData()
    roomUnavailableData.insertSanitizedData(conn)
    conn.addForeignKeyConstraints()
