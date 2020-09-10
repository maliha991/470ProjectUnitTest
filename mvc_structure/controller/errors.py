from flask import render_template
from mvc_structure import mvc_structure, db


@mvc_structure.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@mvc_structure.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
