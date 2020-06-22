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
    try:
      file = self.__get_file('rb')
      directory = pickle.load(file)
      file.close()
      directory.list_of_phones.append(phone_number)
      new_file = self.__get_file('wb')
      pickle.dump(directory, new_file)
      new_file.close()
    except:
      raise Exception('The Directory doesn\'t exist')

  def get_all_phones(self):
    ''' Returns all the phones '''
    try:
      file = self.__get_file('rb')
      directory = pickle.load(file)
      file.close()
      return directory.list_of_phones
    except:
      raise Exception('The Directory doesn\'t exist')

  def get_date_directory(self):
    try:
      file = self.__get_file('rb')
      directory = pickle.load(file)
      file.close()
      return directory.date
    except:
      raise 

  def create_directory(self):
    directory = Directory()
    file = self.__get_file('wb')
    pickle.dump(directory, file)
    file.close()

  def restart_directory(self):
    # try:
      # Getting the current directory
      file = self.__get_file('rb')
      directory = pickle.load(file)
      file.close()
      # Restarting the directory
      directory.restart_directory()
      file = self.__get_file('rb')
      pickle.dump(directory, DATA_FILE)
      file.close()
    # except:
    #   raise Exception('The directory object doesn\'t exist')

  ### Private Methods ###

  def __get_file(self, mode):
    return open(DATA_FILE, mode)
