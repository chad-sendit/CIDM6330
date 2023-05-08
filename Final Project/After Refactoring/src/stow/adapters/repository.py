from abc import ABC, abstractmethod

# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List, Set

from .orm import mapper_registry
from ..domain.models import Pallet


class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set()

    @abstractmethod
    def add_one(pallet) -> None:
        raise NotImplementedError("Derived classes must implement add_one")

    @abstractmethod
    def add_many(pallet) -> None:
        raise NotImplementedError("Derived classes must implement add_many")

    @abstractmethod
    def delete_one(pallet) -> None:
        raise NotImplementedError("Derived classes must implement delete_one")

    @abstractmethod
    def delete_many(pallets) -> None:
        raise NotImplementedError("Derived classes must implement delete_many")

    @abstractmethod
    def get(self, id: int) -> Pallet:
        raise NotImplementedError("Derived classes must implement update")

    @abstractmethod
    def update(pallet) -> int:
        raise NotImplementedError("Derived classes must implement update")

    @abstractmethod
    def update_many(pallets) -> int:
        raise NotImplementedError("Derived classes must implement update_many")

    @abstractmethod
    def find_first(query) -> Pallet:
        raise NotImplementedError("Derived classes must implement find_first")

    @abstractmethod
    def find_all(query) -> list[Pallet]:
        raise NotImplementedError("Derived classes must implement find_all")


# sqlalchemy stuff
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker


class SqlAlchemyRepository(AbstractRepository):
    """
    Uses guidance from the basic SQLAlchemy 2.0 tutorial:
    https://docs.sqlalchemy.org/en/20/tutorial/index.html
    """

    def __init__(self, session, connection_string=None) -> None:
        super().__init__()

        self.engine = None

        # create db connection
        if connection_string != None:
            self.engine = create_engine(connection_string)
        else:
            # let's default to in-memory for now
            self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

        # ensure tables are there
        mapper_registry.metadata.create_all(self.engine)

        # obtain session
        # the session is used for all transactions
        if session != None:
            self.Session = session
        else:
            self.Session = sessionmaker(bind=self.engine)

    def __del__(self):
        self.Session.commit()
        self.Session.close()

    def add_one(self, pallet: Pallet) -> None:
        self.Session.add(pallet)
        self.Session.commit()

    def add_many(self, pallet: list[Pallet]) -> None:
        self.Session.add_all(pallet)
        self.Session.commit()

    def delete_one(self, pallet: Pallet) -> None:
        self.Session.delete(pallet)
        self.Session.commit()

    def delete_many(self, pallets: list[Pallet]) -> None:
        for pallet in pallets:
            self.Session.delete(pallet)

        self.Session.commit()

    def get(self, id: int) -> Pallet:
        # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#get-by-primary-key
        pallet = self.Session.get(Pallet, id)

        if pallet:
            self.seen.add(pallet)

        return pallet

    def update(self, pallet) -> int:
        pass

    def update_many(self, pallets) -> int:
        pass

    def find_first(self, query) -> Pallet:
        pass

    def find_all(self, query) -> list[Pallet]:
        pass