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


def raise_error_if_not_logged_in(session):
    if 'username' not in session.keys():
        raise RuntimeError()


def check_login(username, password):
    # system user: shenweiyang, 123456
    # guest user: lilei, 123456
    import crudapp.model.data_store as dstore
    return dstore.check_user_login(username, password)
