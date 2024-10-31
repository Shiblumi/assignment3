"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_user_email, get_user_id_by_email

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user)
def index():
    return dict(
        load_data_url = URL('load_data'),
        add_item_url = URL('add_item'),
        del_item_url = URL('del_item'),
        toggle_item_url = URL('toggle_item'),
    )


@action('load_data')
@action.uses(db, auth.user)
def load_data():
    user_email = get_user_email()
    item_list = []
    if user_email:
        item_list = db(db.item_list.user_email == user_email).select().as_list()
    return dict(item_list=item_list, user_email=user_email)


@action('add_item', method=['POST'])
@action.uses(db, auth.user)
def add_item():
    item_name = request.json.get('item_name')
    user_email = get_user_email()
    if user_email and item_name:
        id = db.item_list.insert(user_email=user_email, 
                                item_name=item_name)
        return dict(id=id)
    else:
        return "error"


@action('del_item', method=['POST'])
@action.uses(db, auth.user)
def del_item():
    user_email = get_user_email()
    id = request.json.get('id')
    db((db.item_list.id == id ) &
       (db.item_list.user_email == user_email)).delete()
    return "ok"


@action('toggle_item', method=['POST'])
@action.uses(db, auth.user)
def toggle_item():
    user_email = get_user_email()
    id = request.json.get('id')
    is_purchased = request.json.get('is_purchased')
    db((db.item_list.id == id ) &
       (db.item_list.user_email == user_email)).update(is_purchased=is_purchased)
    return "ok"
