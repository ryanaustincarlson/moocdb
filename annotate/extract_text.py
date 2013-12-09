#!/usr/bin/env python

import sys, os
import dbutils, BratAnnotation

try:
    import json
except:
    import simplejson as json

from datetime import datetime
from pprint import pprint

class Text:
    def __init__(self, sql_tuple):
        self.text_id = str(sql_tuple[0]).zfill(4)
        self.text = sql_tuple[1]

    def write(self, username, basedir, cursor):
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        f = open(os.path.join(basedir, self.text_id + '.txt'), 'w')
        f.write(self.text)
        f.close()

        # get annotations
        annotation_file = open(os.path.join(basedir, self.text_id + '.ann'), 'a')
        cursor.execute("SELECT start_pos, end_pos, annotation_type FROM text_annotations WHERE text_id = %s AND annotator = '%s';" % (int(self.text_id), username))
        annotations = cursor.fetchall()
        count = 1
        for start, end, label in annotations:
            annotation_string = "T%d\t%s %s %s\t%s\n" % (count, label, start, end, self.text[start:end])
            annotation_file.write(annotation_string)
            count += 1

        annotation_file.close()

def run(username, sql_query):

    home = os.path.expanduser('~')
    brat = os.path.join(home, 'local/software/brat-v1.3_Crunchy_Frog/data')
    basedir = brat + '/annotate-' + username + '-' + datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")

    db = dbutils.get_database_connection()
    cursor = db.cursor()
    cursor.execute(sql_query)

    texts = [Text(result) for result in cursor.fetchall()]
    for text in texts:
        text.write(username, basedir, cursor)

    # create a config file that encodes (for now) just the username
    config = {'username':username}
    configfile = open(os.path.join(basedir, 'moocdb.conf'), 'w')
    json.dump(config, configfile, indent = 2)
    configfile.close()

    return basedir

def main(args):
    if len(args[1:]) != 2:
        usage = "usage: " + args[0] + "<username> <SQL-query>\n"
        usage += "* username should uniquely identify you\n"
        usage += "* make sure SQL-query is quoted\n"
        usage += "* always make sure you select exactly (text_id, raw_text)\n"
        usage += "* should be something like:\n"
        usage += '\t"SELECT text_id, raw_text FROM moocdb.posts, moocdb.texts where posts.text_id = texts.id and posts.source_id = 2;"\n'

        sys.stderr.write(usage)
        return 1

    username = args[1]
    cmd = args[2]
        
    print run(username, cmd)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
