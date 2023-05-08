from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import date, timedelta

from ..domain import commands, models
from ..adapters import orm, repository
from ..services import handlers, unit_of_work

bp = Blueprint('flaskapi',__name__)

@bp.route('/')
def index():
    return render_template('templates/index.html')

@bp.route('/add_pallet')
def addPallet():
    if request.method == 'POST':
        storageSpot = request.form['storageSpot']
        category = request.form['category']
        notes = request.form['notes']
        error = None

        if not storageSpot:
            error = 'Store spot ID is required.'

        if not category:
            error = 'Category is required.'

        if error is not None:
            flash(error)
        else:
            date = str(date.today())
            handlers.add_Pallet(
                storageSpot,
                category,
                notes,
                date,
                unit_of_work.SqlAlchemyUnitOfWork(),
            )    
            return redirect(url_for('flaskapi.index'))

    return render_template('templates/add.html')

@bp.route('/remove_pallet')
def removePallet():
    if request.method == 'POST':
        storageSpot = request.form['storageSpot']
        error = None

        if not storageSpot:
            error = 'Store spot ID is required.'

        if error is not None:
            flash(error)
        else:
            date = str(date.today())
            handlers.Remove_pallet(
                storageSpot,
                unit_of_work.SqlAlchemyUnitOfWork(),
            )    
            return redirect(url_for('flaskapi.index'))

    return render_template('templates/remove.html')
        
@bp.route('/edit_pallet')
def editPallet():
    return render_template('templates/edit.html')

@bp.route('/all_pallets')
def allPallets():
    return commands.ListPalletsCommand(criteria={'date_added': f'<={date.today()-timedelta(days=30)}'}).execute()

@bp.route('/expired_pallets')
def expiredPallets():
    return commands.ListExpiredPalletsCommand(order_by="storage_spot").execute()