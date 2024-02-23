"""Data extraction module for csv, xlsx, sqlite and json files for Phase 1.

This module was developed for the term project - Hotel Analytics Systems for
CIIC4060/ICOM 5016. This module is exclusively for implementing the objectives
in phase 1 of the project.
"""
import sqlite3
from typing import List


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
        """Connect to database and sanitize input."""
        self.conn = sqlite3.connect("./Raw_Data/reserve.db")
        self.cursor = self.conn.cursor()
        raw_data = self.cursor.execute("""select reid,
        ruid, clid, total_cost, payment, guests from reserve;""").fetchall()
        raw_data: List[ReserveTableData] = list(
            map(lambda x: ReserveTableData(x[0], x[1], x[2], x[3], x[4], x[5]),
                raw_data))
        self.cleanData: List[ReserveTableData] = list(
            filter(
                lambda x: x.reid is not None and x.ruid is not None and x.clid
                is not None and x.total_cost is not None and x.payment is
                not None and x.payment != "" and x.guests is not None and x.
                guests >= 1, raw_data))

    def __del__(self):
        """Disconnect from reserve.db sqlite database."""
        self.conn.close()

    def getCleanData(self) -> List[ReserveTableData]:
        """Get sanitized records from records.db sqlite database."""
        return self.cleanData