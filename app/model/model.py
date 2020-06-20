import pickle
from os import system
from datetime import datetime

DATA_FILE = 'app/data/data.pickle'

class Directory:
  def __init__(self):
    self.date = datetime.now()
    self.list_of_phones = []

  def restart_directory(self):
    self.date = datetime.now()
    self.list_of_phones = []

class Model:
  ''' Abstracion of the model '''
  def save_new_phone(self, phone_number):
    ''' Returns all the phones '''
    directory = Directory()
    try:
      file = self.__get_file('rb')
      directory = pickle.load(file)
      file.close()
      directory.list_of_phones.append(phone_number)
      new_file = self.__get_file('wb')
      pickle.dump(directory, new_file)
      new_file.close()
    except EOFError:
      new_file = self.__get_file('wb')
      directory.list_of_phones.append(phone_number)
      pickle.dump(directory, new_file)
      new_file.close()

  def get_all_phones(self):
    try:
      archivo = self.__get_file('rb')
      directory = pickle.load(archivo)
      archivo.close()
      return directory.list_of_phones
    except IOError:
      return []

  ### Privates Methods ###

  def __get_file(self, mode):
    return open(DATA_FILE, mode)