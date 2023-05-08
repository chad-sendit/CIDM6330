from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Callable, Dict, List, Type

from ..domain import commands, events, models
from ..domain.commands import EditLocationCommand
from ..domain.events import PalletEdited

if TYPE_CHECKING:
    from . import unit_of_work


def add_Pallet(
    cmd: commands.AddPalletCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        # look to see if we already have this bookmark as the title is set as unique
        pallet = uow.storageSpots.get(storage_spot=cmd.storage_spot)
        if pallet is None:
            pallet = models.Bookmark(
                cmd.storage_spot, cmd.category, cmd.date_added, cmd.notes
            )
            uow.storageSpots.add(pallet)
        uow.commit()


# ListBookmarksCommand: order_by: str order: str
def list_Pallet(
    cmd: commands.ListPalletsCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    Pallet = None
    with uow:
        pallets = uow.pallets.all()

    return pallets


# DeleteBookmarkCommand: id: int
def Remove_pallet(
    cmd: commands.RemovePalletCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        pass


# EditBookmarkCommand(Command):
def edit_pallet(
    cmd: commands.EditLocationCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        pass


EVENT_HANDLERS = {
    events.PalletAdded: [add_Pallet],
    events.PalletListed: [list_Pallet],
    events.PalletDeleted: [Remove_pallet],
    events.PalletEdited: [edit_pallet],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.AddPalletCommand: add_Pallet,
    commands.ListPalletsCommand: list_Pallet,
    commands.RemovePalletCommand: Remove_pallet,
    commands.EditLocationCommand: edit_pallet,
}  # type: Dict[Type[commands.Command], Callable]