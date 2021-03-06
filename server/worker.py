#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import mimetypes
import cgi
import os.path

class Worker():

    def __init__(self, http_handler, route_params, url_query):

        # Keep handler to get more data
        self.http_handler = http_handler

        # Request data
        self.request_headers = http_handler.headers
        self.route_params    = route_params
        self.url_query       = url_query

        # e.g: ?key=value_1&key=value_2
        # self.url_query = dict(parse.parse_qs(url_query_str))    # {"key":["value_1", "value_2"]}
#        self.url_query = dict(parse.parse_qs(url_query_str))   # {"key": "value_2"}

    def get_request_header(self, key, default=None):
        return self.request_headers.get(key, default)

    def get_route_param(self, key, default=None):
        return self.route_params.get(key, default)

    def get_url_query(self, key, default=None):
        result = self.url_query.get(key)
        if result == None:
            return result

        if len(result) == 1:
            return result[0]
        else:
            return result


    def format_message(self, code, message=None, data=None):
        output = {
            'status'  : code,
            'message' : message,
            'data'    : data,
        }
        return json.dumps(output)

    def debug(self, message):
        self.http_handler.send_debug_message(message + "\n")


    def addResponseHeader(self, header, value):
        self.http_handler.response_headers[header] = value


    def responseOK(self, data='', message='OK'):
        self.http_handler.send_message(200, message=message, data=data)


    def response(self, data):
        pass

    def responseError(self, error_code, message='', data=''):
        self.http_handler.send_error(error_code, message, data)


    def responseFile(self, file_path, block_size=2048):
        mime_type = mimetypes.guess_type(file_path)[0]
        size      = os.stat(file_path).st_size

        with open(file_path, 'rb') as f:
            self.http_handler.send_headers(200)
            while True:
                data = f.read(block_size)
                if data:
                    self.http_handler.send_data(data)
                else:
                    break
        f.closed


    def getRequestBody(self):
        content_length = int(self.request_headers.get('Content-Length', 0))
        if content_length == 0:
            return None

        content_type = self.request_headers.get('Content-Type', '')
        if content_type == '':
            return None

        ctype, pdict = cgi.parse_header(content_type)

        if ctype == 'multipart/form-data':
            result = None
            form = cgi.FieldStorage(fp=self.http_handler.rfile,
                                    headers=self.http_handler.headers,
                                    environ={
                                        'REQUEST_METHOD':self.http_handler.command,
                                        'CONTENT_TYPE':content_type
                                    })
            # Parse data to dict
            for key in form:
                payload = form[key]
                if type(payload) is list:
                    for item in payload:
                        if result:
                            data = {}
                            data['file_name'] = item.filename
                            data['name'] = item.name
                            data['content'] = item.value
                            result.append(data)
                        else:
                            result= []
                            data = {}
                            data['file_name'] = item.filename
                            data['name'] = item.name
                            data['content'] = item.value
                            result.append(data)
                else:
                    if result:
                        data = {}
                        data['file_name'] = payload.filename
                        data['name'] = payload.name
                        data['content'] = payload.value
                        result.append(data)
                    else:
                        result= []
                        data = {}
                        data['file_name'] = payload.filename
                        data['name'] = payload.name
                        data['content'] = payload.value
                        result.append(data)

            return result

        # application/x-www-form-urlencoded can be complex ...
        # Just return for developer to parse :)
        return self.http_handler.rfile.read(content_length)
