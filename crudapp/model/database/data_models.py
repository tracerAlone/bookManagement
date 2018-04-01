#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sqa

import database


#
# user
class User(database.Base):
    __tablename__ = 'User'
    user_id = sqa.Column(sqa.Integer,
                         primary_key=True)

    # username
    username = sqa.Column(sqa.String(50, convert_unicode=True),
                          nullable=False, index=True)

    # password
    password = sqa.Column(sqa.String(50, convert_unicode=True),
                          nullable=False, index=True)

    # privilege, 1: admin 2: guest
    privilege = sqa.Column(sqa.Integer,
                           primary_key=True)


# create the model for Event
class Event(database.Base):
    __tablename__ = 'Event'
    event_id = sqa.Column(sqa.Integer,
                          primary_key=True)

    # event name
    name = sqa.Column(sqa.String(50, convert_unicode=True),
                      nullable=False, index=True)

    # original capacities
    ori_cap = sqa.Column(sqa.INT,
                         nullable=False, index=True)

    # the number of free capacities 
    free_cap = sqa.Column(sqa.INT,
                          nullable=False, index=True)

    # status, 0: unpublished 1: published
    status = sqa.Column(sqa.INT,
                        nullable=False, index=True)

    # per price per capacity 
    price = sqa.Column(sqa.INT,
                       nullable=False, index=True)

    # the promotional code
    code = sqa.Column(sqa.String(256, convert_unicode=True),
                      nullable=False, index=True)

    #  useless
    p_date = sqa.Column(sqa.String(256, convert_unicode=True),
                        nullable=True, index=True)


class Info(database.Base):
    __tablename__ = 'info'
    info_id = sqa.Column(sqa.Integer,
                         primary_key=True)

    # user name
    user_name = sqa.Column(sqa.String(50, convert_unicode=True),
                           nullable=False, index=True)

    # event_id 
    event_id = sqa.Column(sqa.INT,
                          nullable=False, index=True)

    # using code
    code = sqa.Column(sqa.String(256, convert_unicode=True),
                      nullable=False, index=True)

    # cost 
    cost = sqa.Column(sqa.INT,
                      nullable=False, index=True)
