from pg8000 import DBAPI
import sys

SOURCE_COURSERA = 1

#def get_database_connection(host='localhost', user='rcarlson', password='', database='moocdb'):
def get_database_connection(unix_sock='/tmp/.s.PGSQL.5432', user='rcarlson', password='', database='moocdb'):
    '''
        NOTE: right now (2013-11-29) localhost doesn't resolve properly so we
              need to point to the socket file address. hopefully in the future we
              can get the host working so that we don't have to specify this ugly
              file handle.
    '''
    db = DBAPI.connect(
            unix_sock=unix_sock,
            #host=host,
            user=user,
            password=password,
            database=database)
    return db

def insert_into_table(cursor, table, columns, values):
    def format_text(text):
        return "'" + text.replace("'", "''").replace("%", "%%") + "'"

    columns_string = "(" + ', '.join([str(c) for c in columns]) + ")" \
            if columns is not None else ""

    values_string = "(" + ', '.join([format_text(v) if type(v) in [str, unicode] else str(v) for v in values]) + ")"

    insert_cmd = "INSERT INTO {0} {1} VALUES {2} RETURNING id;".format(table, columns_string, values_string)
    sys.stderr.write(insert_cmd + '\n')

    cursor.execute(insert_cmd)
    return cursor.fetchone()[0]


