from flask import jsonify, make_response
from flask_restful import reqparse, abort, Resource
from sys import path
from datetime import datetime
from os import environ
path.append('./api')
from api.model.model import Model
from sentry_sdk import capture_exception

parser = reqparse.RequestParser()
parser.add_argument('phone')

class Validator(Resource):
    ''' Abstraction of a Validator '''
    def __init__(self):
        super().__init__()
        self.response = {}
        self.model = Model()

    def get(self):
        ''' Checks the sended phone number '''
        # Arguments
        args = parser.parse_args()
        # Validating the args
        if args['phone'] == '' or len(args.keys()) == 0 or args['phone'] == None:
            self.response['status'] = 400
            self.response['error'] = True
            self.response['message'] = 'Caller id not found or null'
            return jsonify(self.response)
        # Initialiting the directory
        self.response['messages'] = []
        try:
            self.__init_register(datetime.now())
        except Exception:
            self.model.create_directory()
            self.response['messages'].append('[INFO]: The Directory was created currently')
        # Searching the number
        try:
            if self.__search_number(args['phone']):
                self.response['status'] = 200
                self.response['error'] = False
                self.response['new_contact'] = False
            else:
                # Saving the new number
                self.model.save_new_phone(str(args['phone']))
                self.response['status'] = 201
                self.response['error'] = False
                self.response['new_contact'] = True
        except Exception as e:
            # Restarting the method
            self.response['status'] = 400
            self.response['error'] = True
            self.response['messages'].append(str(e))
            capture_exception(e)
        return make_response(jsonify(self.response), self.response['status'])

    ### Privates Methods ###

    def __init_register(self, date):
        try:
            dir_date = self.model.get_date_directory()
            if dir_date.strftime('%Y-%m-%d') != date.strftime('%Y-%m-%d'):
                self.model.restart_directory()
                self.response['messages'].append('[INFO]: The directory was restarted')
        except Exception as e:
            raise e

    def __search_number(self, phone_number):
        try:
            return self.model.search_phone(str(phone_number))
        except Exception as e:
            raise e
    