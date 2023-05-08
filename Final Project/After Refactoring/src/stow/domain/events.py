from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .models import Pallet

# from database import DatabaseManager

# module scope
# db = DatabaseManager("bookmarks.db")


class Event(ABC):
    pass


@dataclass
class PalletAdded(Event):
    storage_spot: int
    category: str
    date_added: datetime
    notes: Optional[str] = None


@dataclass
class PalletEdited(Event):
    storage_spot: int
    category: str
    date_added: datetime
    notes: Optional[str] = None


@dataclass
class PalletListed(Event):
    pallets: list[Pallet]


@dataclass
class PalletDeleted(Event):
    pallet: Pallet


# @dataclass
# class BookmarksDeleted(Event):
#     bookmarks: list[Bookmark]