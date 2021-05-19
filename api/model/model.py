import pickle
import sqlite3
from os import system
from datetime import datetime
from contextlib import closing

DATA_FILE   = 'api/data/data.pickle'
DB_FILE     = 'api/data/directory.db'
READ_MODE   = 'rb'
WRITE_MODE  = 'wb'

class Directory:
    def __init__(self):
        self.date = datetime.now()
        self.log_date = datetime.now()

    def restart_directory(self):
        self.date = datetime.now()

    def restart_log_date(self):
        self.log_date = datetime.now()

class Model:
    ''' Abstracion of the model '''
    DIRECTORY_ERROR = "The Directory doesn't exist"
    SEARCH_QUERY    = "SELECT phone FROM directory WHERE phone = '%s'"
    INSERT_STMT     = "INSERT INTO directory VALUES ('%s')"
    DELETE_STMT     = "DELETE FROM directory"

    def get_date_directory(self):
        try:
            return self.__get_directory().date
        except:
            raise Exception(self.DIRECTORY_ERROR)

    def restart_directory(self):
        try:
            # Getting the current directory
            directory = self.__get_directory()
            # Restarting the directory
            directory.restart_directory()
            self.__execute_sql_stmt(self.DELETE_STMT, False)
            self.__update_directory(directory)
        except:
            raise Exception(self.DIRECTORY_ERROR)

    def create_directory(self):
        directory = Directory()
        self.__update_directory(directory)

    def search_phone(self, phone_number):
        try:
            return len(self.__execute_sql_stmt((self.SEARCH_QUERY %(phone_number)), True)) > 0
        except Exception as e:
            raise e
  
    def save_new_phone(self, phone_number):
        try:
            self.__execute_sql_stmt((self.INSERT_STMT %(phone_number)), False)
        except Exception as e:
            raise e

    ### Private Methods ###

    def __get_file(self, mode):
        return open(DATA_FILE, mode)

    def __get_directory(self):
        file = self.__get_file(READ_MODE)
        directory = pickle.load(file)
        file.close()
        return directory

    def __update_directory(self, directory):
        file = self.__get_file(WRITE_MODE)
        pickle.dump(directory, file)
        file.close()

    def __execute_sql_stmt(self, statement, is_query):
        result = None
        with closing(sqlite3.connect(DB_FILE)) as connection:
            with closing(connection.cursor()) as cursor:
                result = cursor.execute(statement)
                if is_query:
                    result = result.fetchall()
                connection.commit()
        return result

