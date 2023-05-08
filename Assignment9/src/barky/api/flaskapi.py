from . baseapi import AbstractBookMarkAPI
from ..domain import commands

from ..adapters import repository
from ..services import services
from ..services import unit_of_work


import functools
from flask_sqlalchemy import SQLAlchemy

from flask import (
    Flask,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
bp = Blueprint('flask_bookmark_api', __name__, url_prefix='/api')

class FlaskBookmarkAPI(AbstractBookMarkAPI):
    """
    Flask - the beginnings of a Flask implementation is shown below. 
    Actual action responses would replace the starter methods below.
    """
    def __init__(self) -> None:
        super().__init__()
    

    def index(self):
        # Call the 'ListBookmarks' Command from commands.py
        return commands.ListBookmarksCommand().execute() 

    def one(self, id):
        return f'The provided id is {id}'

    def all(self):
        return f'all records'

    # @app.route('/api/first/<property>/<value>/<sort>')
    def first(self, filter, value, sort):
        return f'the first '
        pass
    
    def many(self, filter, value, sort):
        pass
    
    @bp.route('/add', methods=('GET', 'POST'))
    def add():
        if request.method == 'POST':
            title = request.form['title']
            url = request.form['url']
            notes = request.form['notes']

            if not title:
                error = 'Title is required'
            
            elif not url:
                error = 'URL is required'

            if error is not None:
                flash(error)
            
            else:
                commands.AddBookmarkCommand.execute({'title': title, 'url': url, 'notes': notes})
                return f'Added!'
    
        return render_template('add.html')

    def delete(bookmark):
        pass

    def update(bookmark):
        pass

fb = FlaskBookmarkAPI()
# bp = Blueprint('flask_bookmark_api', __name__, url_prefix='/api')

# @app.route('/api')
bp.add_url_rule('/', 'index', fb.index, ['GET'])

# @app.route('/api/one/<id>')
bp.add_url_rule('/one/<id>', 'one', fb.one, ['GET'])

# @app.route('/api/all')
bp.add_url_rule('/all', 'all', fb.all, ['GET'])

# @app.route('/api/add')
bp.add_url_rule('/add', 'add', fb.add, ['GET'])