from sqlalchemy import Column, Integer, Text
from typing import Dict
from db import db


# Public key model
class PublicKey(db.Model):
    # Columns
    key_id = Column(Integer, primary_key=True)
    pem = Column(Text())

    def __init__(self, pem=None):
        self.pem = pem

    def __repr__(self):
        return '<%r %r>' % (self.key_id, self.pem)

    def as_dict(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def add_key(pem):
    key = PublicKey(pem)
    db.session.add(key)
    db.session.commit()
    return key.key_id


def list_keys():
    result = {}
    keys = PublicKey.query.all()
    for key in keys:
        result[key.key_id] = key.pem
    return result


def get_key(key_id):
    result = {}
    try:
        keys = PublicKey.query.filter_by(key_id=int(key_id))
        for key in keys:
            result[key.key_id] = key.pem
    except ValueError:
        print("Unable to query for key ID: " + repr(key_id))
    return result
