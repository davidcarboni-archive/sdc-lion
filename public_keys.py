import os
import components
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text
from typing import Dict


# service name (initially used for sqlite file name and schema name)
SERVICE_NAME = components.NAME
ENVIRONMENT_NAME = os.getenv('ENVIRONMENT_NAME', 'dev')
PORT = int(os.environ.get('PORT', 5009))


# Enable cross-origin requests
app = Flask(__name__)
CORS(app)


# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv("DATABASE_URL", "sqlite:///:memory:")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()
SCHEMA_NAME = None if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite') \
    else '{}_{}'.format(ENVIRONMENT_NAME, SERVICE_NAME)

if os.getenv('SQL_DEBUG') == 'true':
    import logging
    import sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


# Public key model
class PublicKey(db.Model):
    #__table_args__ = {'schema': SCHEMA_NAME}
    # Columns
    key_id = Column(Integer, primary_key=True)
    pem = Column(Text())

    def __init__(self, pem=None):
        self.pem = pem

    def __repr__(self):
        return '<%r %r>' % (self.key_id, self.pem)

    def as_dict(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

if SCHEMA_NAME is None:
    db.create_all()
    print("Using sqlite test database.")
else:
    print("Database schema name is: " + repr(SCHEMA_NAME))


def add(pem):
    key = PublicKey(pem)
    db.session.add(key)
    db.session.commit()
    return key.key_id


def list():
    result = {}
    keys = PublicKey.query.all()
    for key in keys:
        result[key.key_id] = key.pem
    return result
