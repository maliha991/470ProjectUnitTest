from mvc_structure import app, db
from mvc_structure.model.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
