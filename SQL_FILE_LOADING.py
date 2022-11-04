import pyodbc
import csv


conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};' ### Making Connection
                      'Server=IP;'
                      'Database=DB_NAME;'
                      'PORT=PORT_NUMBER;'
                      'UID=USERNAME;'
                      'PWD=PASSWORD;')
my_cursor = conn.cursor()
print('Cursor established')


def insert_records(table, yourcsv, cursor, cnxn):
    counter = 0
    #INSERT SOURCE RECORDS TO DESTINATION
    with open(yourcsv) as csvfile:
        csvFile = csv.reader(csvfile, delimiter=',')
        header = next(csvFile)
        headers = map((lambda x: x.strip()), header)
        insert = 'INSERT INTO {} ('.format(table) + ', '.join(headers) + ') VALUES '
        for row in csvFile:
            values = map((lambda x: "'"+x.strip()+"'"), row)
            cursor.execute(insert +'('+ ', '.join(values) +');')
            conn.commit() #must commit unless your sql database auto-commits
            counter = counter + 1
            print(counter)

table = 'table_name'
mycsv = r'' # SET YOUR FILEPATH
insert_records(table, mycsv, my_cursor, conn)
my_cursor.close()
print('All Rows Inserted')
