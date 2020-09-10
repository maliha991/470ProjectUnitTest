from mvc_structure import mvc_structure, db
from mvc_structure.model.models import User, Post


@mvc_structure.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
