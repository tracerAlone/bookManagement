#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask

import crudapp.model.curl_print as curl_print


def def_control(app):
    @app.before_request
    def before():
        curl_print.print_incoming_request(flask.request)

    @app.after_request
    def after(response):
        curl_print.print_outgoing_response(response)
        return response
