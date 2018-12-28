import mysql.connector
from mysql.connector import Error

config = {
  'user': 'xxxx',
  'password': 'xxxx',
  'host': 'xxxx',
  'database': 'xxx',
  'raise_on_warnings': True
}

selectStatement = '''SELECT * FROM user'''

def openConnection():
    """ Connect to my sql database """
    print ('In connect')
    conn = None
    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected:
            print("Connection is open")
            return conn
    except Error as error:
        print(f'Something wrong happend {error}')
    return None

def getDataFromDb(cursor):
    cursor.execute(selectStatement)
    for row in cursor.fetchall():
            print(row)

def showResults():
    conn = openConnection()
    if conn != None:
        getDataFromDb(conn.cursor())
        conn.close()
    print ('Example is over')

if __name__== '__main__' : showResults()
