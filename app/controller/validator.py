from flask import jsonify
from flask_restful import reqparse, abort, Resource
from sys import path
from datetime import datetime
path.append('./model')
from model.model import Model

parser = reqparse.RequestParser()
parser.add_argument('task')

class Validator(Resource):
  ''' Abstraction of a Validator '''
  def get(self):
    ''' Returns all the phones '''
    return jsonify({'response': 'Hello World!'})

  def post(self):
    ''' Returns the result of the  '''
    return jsonify({'phones': [{'phone':'094123444'}]})

  ### Privates Methods ###

  def __init_register(self, date):
    pass

  def __search_number(self):
    pass