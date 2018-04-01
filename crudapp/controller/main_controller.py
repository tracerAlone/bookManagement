#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" The controller receives commands from the views,
    sends commands to the model,
    chooses the views to send,
    and sends the views to the user.

    This controller is powered by Flask.

    The views are Jinja2 templates and static files.

"""

import flask

import crudapp.model.data_store as dstore
import crudapp.model.login as log_in

# dstore: Data store
from sqlalchemy.exc import IntegrityError as sqla_IntegrityError

DEBUG = True


def def_control(app):
    # This is part of the data storage initialization
    dstore.teardown(app)

    # login the system
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if flask.request.method == 'GET':
            return flask.render_template('login.html')

        elif flask.request.method == 'POST':
            login_ok, status = log_in.check_login(flask.request.form.get('username', ""),
                                                  flask.request.form.get('password', ""))
            if login_ok:
                flask.session['username'] = flask.request.form['username']
                # status: admin or guest
                flask.session['status'] = status
                return flask.redirect(flask.url_for('index'))
            else:
                flask.flash('Invalid credentials')
                return flask.render_template('login.html')

    # default html for displaying
    @app.route('/')
    def index():
        # Returns main page
        if "username" not in flask.session:
            return flask.redirect(flask.url_for('login'))
        events = dstore.query_all_event(status=flask.session['status'])
        infos = dstore.query_all_info(flask.session['username'], flask.session['status'])
        return flask.render_template('index.html', events=events, infos=infos, status=flask.session['status'])

    @app.route('/search_book', methods=['GET', 'POST'])
    def search_info():
        # Returns main page
        if "username" not in flask.session:
            return flask.redirect(flask.url_for('login'))
        events = dstore.query_all_event(status=flask.session['status'], search=flask.request.form['search'])
        infos = dstore.query_all_info(flask.session['username'])
        return flask.render_template('index.html', events=events, infos=infos, status=flask.session['status'])

    # The data that comes from a method POST is stored by flask in
    @app.route('/add_event', methods=['POST'])
    def add_event():
        log_in.raise_error_if_not_logged_in(flask.session)
        # code is discount
        msg = dstore.add_event(flask.request.form['name'],
                               flask.request.form['ori_cap'],
                               flask.request.form['price'],
                               flask.request.form['code'], )
        # Returns a 300 redirection command with the the url corresponding
        # to function index(). Then the browser will ask for that url.
        if msg is not True:
            return flask.render_template('server_error.html', msg=msg), 200
        return flask.redirect(flask.url_for('index'))

    @app.route('/delete_event', methods=['POST'])
    def delete_event():
        log_in.raise_error_if_not_logged_in(flask.session)
        dstore.delete_event(flask.request.form['event_id'])
        return flask.redirect(flask.url_for('index'))

    @app.route('/publish_event', methods=['POST', 'GET'])
    def publish_event():
        log_in.raise_error_if_not_logged_in(flask.session)
        msg = dstore.publish_event(flask.request.form['event_id'])

        if msg is not True:
            return flask.render_template('server_error.html', msg=msg), 200

        return flask.redirect(flask.url_for('index'))

    @app.route('/book_event', methods=['POST', 'GET'])
    def book_event():
        log_in.raise_error_if_not_logged_in(flask.session)
        msg = dstore.book_event(flask.request.form['event_id'], flask.session['username'])

        if msg is not True:
            return flask.render_template('server_error.html', msg=msg), 200

        return flask.redirect(flask.url_for('index'))

    @app.route('/edit_event', methods=['POST'])
    def edit_event():
        log_in.raise_error_if_not_logged_in(flask.session)
        msg = dstore.edit_event(flask.request.form['event_id'],
                                flask.request.form['name'],
                                flask.request.form['price'],
                                flask.request.form['code'], )

        if msg is not True:
            return flask.render_template('server_error.html', msg=msg), 200

        return flask.redirect(flask.url_for('index'))

    @app.route('/cancel_event', methods=['POST', 'GET'])
    def cancel_event():
        log_in.raise_error_if_not_logged_in(flask.session)
        msg = dstore.cancel_event(flask.request.form['info_id'])
        if msg is not True:
            return flask.render_template('server_error.html', msg=msg), 200

        return flask.redirect(flask.url_for('index'))

    @app.route('/logout')
    def logout():
        # remove the username from the session if it's there
        flask.session.pop('username', None)
        flask.session.pop('status', None)
        return flask.redirect(flask.url_for('index'))

    # set the secret key.  keep this really secret:
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    @app.errorhandler(404)
    def page_not_found(error):
        if DEBUG:
            raise
        return flask.render_template('page_not_found.html'), 404

    # @app.errorhandler(flask.DatabaseError)
    # def special_exception_handler(error):
    #     return 'Database connection failed', 500

    @app.errorhandler(sqla_IntegrityError)
    def integrity_exception_handler(error_msg):
        msg = 'Error: field must be unique'
        if DEBUG:
            raise
        return flask.render_template('server_error.html', msg=msg), 500

    @app.errorhandler(AssertionError)
    def validation_exception_handler(error_msg):
        if DEBUG:
            raise
        return flask.render_template('server_error.html', msg=error_msg), 500

    @app.errorhandler(RuntimeError)
    def login_exception_handler(error_msg):
        msg = 'You are not logged in'
        if DEBUG:
            raise
        return flask.render_template('server_error.html', msg=msg), 500
