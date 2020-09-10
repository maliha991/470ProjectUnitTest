import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config



mvc_structure = Flask(__name__, template_folder='./view')
mvc_structure.config.from_object(Config)
db = SQLAlchemy(mvc_structure)
migrate = Migrate(mvc_structure, db)
login = LoginManager(mvc_structure)
login.login_view = 'login'
mail = Mail(mvc_structure)
bootstrap = Bootstrap(mvc_structure)
moment = Moment(mvc_structure)

if not mvc_structure.debug:
    if mvc_structure.config['MAIL_SERVER']:
        auth = None
        if mvc_structure.config['MAIL_USERNAME'] or mvc_structure.config['MAIL_PASSWORD']:
            auth = (mvc_structure.config['MAIL_USERNAME'], mvc_structure.config['MAIL_PASSWORD'])
        secure = None
        if mvc_structure.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(mvc_structure.config['MAIL_SERVER'], mvc_structure.config['MAIL_PORT']),
            fromaddr='no-reply@' + mvc_structure.config['MAIL_SERVER'],
            toaddrs=mvc_structure.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        mvc_structure.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    mvc_structure.logger.addHandler(file_handler)

    mvc_structure.logger.setLevel(logging.INFO)
    mvc_structure.logger.info('Microblog startup')

from mvc_structure.controller import errors, routes
from mvc_structure.model import models
