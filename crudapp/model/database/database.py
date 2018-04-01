#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy as sqa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dcl

# CAMBIANDO echo se cambia los logs que hace sqlalchemy
engine = sqa.create_engine('sqlite:///database.db', echo=False)

#
db_session = orm.scoped_session(orm.sessionmaker(autocommit=False,
                                                 autoflush=False,
                                                 bind=engine))

Base = dcl.declarative_base()

Base.query = db_session.query_property()


# def populate():

#     session = Session()

#     person = models.Person(firstname='Barack', lastname='Obama')
#     session.add(person)

#     person = models.Person(firstname='Mitt', lastname='Romney')
#     session.add(person)

#     session.commit()

#     session.close()


def init_db():
    import data_models
    Base.metadata.create_all(engine)


init_db()


# if __name__ == '__main__':
#     populate()
