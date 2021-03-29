import sqlite3
import pickle
from contextlib import closing
from api.model.model import Directory

DATA_FILE   = 'api/data/data.pickle'
DB_FILE     = 'api/data/directory.db'
WRITE_MODE  = 'wb'

if __name__ == '__main__':
    # SQLite3 Configuration
    try:
        with closing(sqlite3.connect(DB_FILE)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute('CREATE TABLE directory (phone TEXT)')
                connection.commit()
    except:
        pass
    # Pickle Configuration
    directory = Directory()
    file = open(DATA_FILE, WRITE_MODE)
    pickle.dump(directory, file)
    file.close()
