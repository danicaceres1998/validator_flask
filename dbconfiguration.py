import sqlite3

if __name__ == '__main__':
    conection = sqlite3.connect('api/data/directory.db')
    cursor = conection.cursor()
    try:
        cursor.execute('CREATE TABLE directory (phone TEXT)')
    except:
        pass
