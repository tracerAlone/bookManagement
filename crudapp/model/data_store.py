#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The model receives commands from the controller,
    and interacts with the host computer:
    - reads data from db
    - writes data
    - writes to console
    - logs
    - etc

    The db model is built using SQLAlchemy
"""

from crudapp.model.database import database
from crudapp.model.database.data_models import Event, Info, User
import time

database.init_db()
session = database.db_session


def teardown(app):
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()


# dal for user
def check_user_login(username, password):
    users = session.query(User).filter_by(username=username).filter_by(password=password).all()
    if not users:
        return False, ""

    current_user = users[0]
    return True, "admin" if current_user.privilege == 1 else "guest"


# end


def query_all_event(status, search=None):
    if status == "guest":
        if search:
            return Event.query.filter_by(status=1).filter(Event.name.like("%%%s%%" % search)).all()
        else:
            return Event.query.filter_by(status=1).all()
    else:
        if search:
            return Event.query.filter(Event.name.like("%%%s%%" % search)).all()
        else:
            return Event.query.all()


def query_all_info(username, status=None):
    if status == 'admin':
        return session.query(Info).all()
    else:
        return session.query(Info).filter_by(user_name=username).all()


def add_event(name, ori_cap, price, code):
    """
    :param name:
    :param ori_cap: amount left
    :param price:
    :param code:
    :param p_date:
    :return:
    """
    try:
        c = int(ori_cap)
        if c <= 0:
            raise Exception("err")
    except:
        return "capacity must be integer"

    try:
        # code is discount
        x = int(code)
        if x > 100:
            raise Exception("err")
        elif x < 0:
            raise Exception("err")
    except:
        return "discount must be integer, [1-100]"

    status = 0  # unpublished
    np = Event(name=name,
               ori_cap=ori_cap,
               free_cap=ori_cap,
               price=price,
               code=code,
               status=status,
               p_date="")
    session.add(np)
    session.commit()
    return True


def delete_event(event_id):
    """
    :param event_id: book_id
    :return:
    """
    q = session.query(Event).filter_by(
        event_id=event_id
    ).one()
    session.delete(q)
    cs = session.query(Info).filter_by(
        event_id=event_id
    ).all()
    for c in cs:
        session.delete(c)
    session.commit()
    return True


def cancel_event(info_id):
    p = session.query(Info).filter_by(
        info_id=info_id
    ).one()
    event_id = p.event_id
    session.delete(p)
    q = session.query(Event).filter_by(
        event_id=event_id
    ).one()
    q.free_cap += 1
    session.commit()
    return True


def publish_event(event_id):
    p = session.query(Event).filter_by(
        event_id=event_id
    ).one()
    p.status = 1
    session.commit()
    return True


def book_event(event_id, user_name):
    p = session.query(Event).filter_by(
        event_id=event_id
    ).one()
    # 0: unpublish 1: publish
    if p.status == 0:
        return "this book is not in store, please try later"

    free_cap = p.free_cap
    if free_cap > 0:
        p.free_cap -= 1
    else:
        return "there are no capacities for this book!"

    # price could be reduce if there is an code
    cost = p.price
    discount = p.code
    cost = int(int(cost) * int(discount) / 100)
    n = Info(
        user_name=user_name,
        event_id=event_id,
        code=p.code,
        cost=cost,
    )
    session.add(n)
    session.commit()
    return True


def edit_event(event_id, name, price, code):
    """
    :param event_id: book_id
    :param name:
    :param price:
    :param code: discount
    :return:
    """
    p = session.query(Event).filter_by(
        event_id=event_id
    ).one()

    try:
        # code is discount
        x = int(code)
        if x > 100:
            raise Exception("err")
        elif x < 0:
            raise Exception("err")
    except:
        return "discount must be integer, [1-100]"

    p.name = name
    p.price = price
    p.code = code
    session.commit()
    return True
