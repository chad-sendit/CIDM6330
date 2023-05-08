import logging
from typing import Text

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Text

# from sqlalchemy.orm import mapper
from sqlalchemy.orm import registry

from ..domain.models import Pallet

logger = logging.getLogger(__name__)

metadata = MetaData()

mapper_registry = registry()


"""
Pure domain bookmark:
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
url TEXT NOT NULL,
notes TEXT,
date_added TEXT NOT NULL
date_edited TEXT NOT NULL
"""
storageSpots = Table(
    "storageSpots",
    mapper_registry.metadata,
    Column("storage_spot", Integer, primary_key=True),
    Column("category", String(255)),
    Column("notes", Text),
    Column("date_added", DateTime),
)


def start_mappers():
    logger.info("string mappers")
    # SQLAlchemy 2.0
    storageSpots_mapper = mapper_registry.map_imperatively(Pallet, storageSpots)
    # SQLAlchemy 1.3
    # bookmarks_mapper = mapper(Bookmark, bookmarks)