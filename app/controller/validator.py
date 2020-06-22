from flask import jsonify
from flask_restful import reqparse, abort, Resource
from sys import path
from datetime import datetime
path.append('./model')
from app.model.model import Model

parser = reqparse.RequestParser()
parser.add_argument('phone')

class Validator(Resource):
  ''' Abstraction of a Validator '''
  def __init__(self):
    super().__init__()
    self.response = {}
    self.model = Model()

  def get(self):
    ''' Returns all the phones '''
    # Getting the list of phones
    try:
      self.response['phones'] = self.model.get_all_phones()
      self.response['status'] = 200
      self.response['error'] = False
    except Exception as e:
      self.response['status'] = 500
      self.response['error'] = True
      self.response['messages'] = str(e) + '. Please try again.'
      self.model.create_directory()
    # Returning the response
    return jsonify(self.response)

  def post(self):
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
    self.response['messages'].append(args)
    try:
      self.__init_register(datetime.now())
      self.response['messages'].append('SUCCESS -> The Directory started successfully')
    except Exception as e:
      self.model.create_directory()
      self.response['messages'].append('ERROR -> The Directory was created currently')
    # Searching the number
    try:
      phone = self.__search_number(args['phone'])
      if len(phone) == 0:
        # Saving the new number
        self.model.save_new_phone(args['phone'])
        self.response['status'] = 201
        self.response['error'] = False
        self.response['new_contact'] = True
      else:
        self.response['status'] = 200
        self.response['error'] = False
        self.response['new_contact'] = False
    except Exception:
      # Restarting the method
      self.post()
    else: 
      return jsonify(self.response)

  ### Privates Methods ###

  def __init_register(self, date):
    try:
      dir_date = self.model.get_date_directory()
      if dir_date.strftime('%Y-%m-%d') != date.strftime('%Y-%m-%d'):
        self.response['messages'].append('The directory was restarted')
        self.model.restart_directory()
    except Exception as e:
      raise e

  def __search_number(self, phone_number):
    try:
      phones_list = self.model.get_all_phones()
      phone = list(ph for ph in phones_list if phone_number == ph)
      return phone
    except Exception as e:
      raise e
    