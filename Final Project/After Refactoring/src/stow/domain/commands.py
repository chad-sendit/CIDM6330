"""
This module utilizes the command pattern - https://en.wikipedia.org/wiki/Command_pattern - to 
specify and implement the business logic layer
"""
import sys
from abc import ABC, abstractmethod
from datetime import date, timedelta

from services.database import DatabaseManager

# module scope
db = DatabaseManager("storageSpots.db")


class Command(ABC):
    @abstractmethod
    def execute(self, data):
        raise NotImplementedError("A command must implement the execute method")


class CreateStorageSpotsTableCommand(Command):
    """
    uses the DatabaseManager to create the storageSpots table
    """

    def execute(self, data=None):
        db.create_table(
            "storageSpots",
            {
                "storage_spot": "integer primary key",
                "category": "text not null",
                "notes": "text",
                "date_added": "date not null",
            },
        )


class AddPalletCommand(Command):
    """
    This class will:
    1. Expect a dictionary containing the title, URL, and (optional) notes information for a bookmark.
    2. Add the current datetime to the dictionary as date_added.
    3. Insert the data into the bookmarks table using the DatabaseManager.add method.
    4. Return a success message that will eventually be displayed by the presentation layer.
    """

    def execute(self, data, timestamp=None):
        data["date_added"] = str(date.today())
        db.add("storageSpots", data)
        return "Pallet added!"


class ListPalletsCommand(Command):
    """
    We need to review the bookmarks in the database.
    To do so, this class will:
    1. Accept the column to order by, and save it as an instance attribute.
    2. Pass this information along to db.select in its execute method.
    3. Return the result (using the cursor’s .fetchall() method) because select is a query.
    """

    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self, data=None):
        return db.select("storageSpots", order_by=self.order_by).fetchall()


class ListExpiredPalletsCommand(Command):
    """
    We need to review the bookmarks in the database.
    To do so, this class will:
    1. Accept the column to order by, and save it as an instance attribute.
    2. Pass this information along to db.select in its execute method.
    3. Return the result (using the cursor’s .fetchall() method) because select is a query.
    """

    def __init__(self, criteria={'date_added': f'<={date.today()-timedelta(days=30)}'}):
        self.criteria = criteria

    def execute(self, data=None):
        return db.select("storageSpots", criteria=self.criteria).fetchall()


class RemovePalletCommand(Command):
    """
    We also need to remove bookmarks.
    """

    def execute(self, data):
        db.delete("storageSpots", {"storage_spot": data})
        return "Pallet Removed!"


class EditLocationCommand(Command):
    def execute(self, data):
        db.dbUpdate(
            "storageSpots",
            data,
        )
        return "Location updated!"


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()