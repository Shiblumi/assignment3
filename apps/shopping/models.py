"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def get_user_id_by_email(email):
    user = db(db.users.email == email).select().first()
    return user.id if user else None

db.define_table('item_list',
    Field('item_name', requires=IS_NOT_EMPTY()),
    Field('is_purchased', 'boolean', default=False),
    Field('user_email', 'string', unique=True),
    )

db.commit()
