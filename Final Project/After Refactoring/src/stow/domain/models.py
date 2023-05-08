from datetime import datetime


class Pallet:
    """
    Pure domain bookmark:
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    notes TEXT,
    date_added TEXT NOT NULL
    date_edited TEXT NOT NULL
    """

    def __init__(
        self,
        storage_spot: int,
        category: str,
        notes: str,
        date_added: datetime,
    ) -> None:
        self.storage_spot = storage_spot
        self.category = category
        self.notes = notes
        self.date_added = date_added