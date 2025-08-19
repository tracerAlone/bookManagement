#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap
import pprint
import json

LINE_LENGTH = 80


def print_incoming_request(request):
    print('\n\n')
    print('< {} {} {}'.format(request.method,
                               request.url, request.full_path))
    for k, v in request.headers:
        print(wrap_header(k, v, '<'))

    # print(request.headers['content-type'])
    # print('')

    if request.mimetype == 'application/json':
        print('< request data is json:')
        print(wrap_json(request.data, '<'))

    elif request.mimetype == 'application/x-www-form-urlencoded':
        print('< request data is x-www-form-urlencoded:')
        print(request.form)

    else:
        pass

    print('')


def print_outgoing_response(response):
    print('> %s' % response.status)
    for k, v in response.headers:
        print(wrap_header(k, v, '>'))

    if response.mimetype == 'application/json':
        print('> response data is json:')
        print(wrap_json(response.data, '>'))


def wrap_json(json_string, sign):
    pprinted = pprint.pformat(
        json.loads(json_string), width=LINE_LENGTH).split('\n')
    spaced = ['{} {}'.format(sign, l) for l in pprinted]
    finished = []
    for line in spaced:
        indent = line.find(':') + 4
        line_wrapped = textwrap.fill(
            line, LINE_LENGTH, subsequent_indent=' ' * indent)
        finished.append(line_wrapped)
        # spaced = ['{} {}'.format(sign, l) for l in line_wrapped]

    return '\n'.join(finished)


def wrap_header(header, value, sign):
    interm = '%s: %s' % (header, value)
    indent = len(header) + 2
    wrapped = textwrap.wrap(
        interm, LINE_LENGTH, subsequent_indent=' ' * indent)
    spaced = ['{} {}'.format(sign, l) for l in wrapped]

    return '\n'.join(spaced)
