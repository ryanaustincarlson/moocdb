import MySQLdb
import sys

def get_database_connection(host='localhost', unix_sock='/var/tmp/mysql.sock', user='root', password='', database='moocdb'):
    '''
        NOTE: right now (2013-11-29) localhost doesn't resolve properly so we
              need to point to the socket file address. hopefully in the future we
              can get the host working so that we don't have to specify this ugly
              file handle.
    '''
    try:
        db = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=database)
    except:
        db = MySQLdb.connect(
            unix_socket=unix_sock,
            user=user,
            passwd=password,
            db=database)

    return db

def insert_into_table(cursor, table, columns, values):
    def format_text(text):
        return "'" + text.replace("'", "''").replace("%", "%%") + "'"

    columns_string = "(" + ', '.join([str(c) for c in columns]) + ")" \
            if columns is not None else ""

    values_string = "(" + ', '.join([format_text(v) if type(v) in [str, unicode] else str(v) for v in values]) + ")"

    #insert_cmd = "INSERT INTO {0} {1} VALUES {2};".format(table, columns_string, values_string)
    insert_cmd = "INSERT INTO " + table + " " + columns_string + " VALUES " + values_string + ";"
    sys.stderr.write(insert_cmd + '\n')

    cursor.execute(insert_cmd)
    cursor.execute("SELECT last_insert_id();")
    return cursor.fetchone()[0]


