#!/usr/bin/env python

import sys, os, shutil
import dbutils

try:
    import json
except:
    import simplejson as json

from pprint import pprint
from BratAnnotation import BratAnnotation

def run(annotation_dir):
    # load username from config
    configfile = open(os.path.join(annotation_dir, 'moocdb.conf'))
    config = json.load(configfile)
    configfile.close()
    username = config['username']

    annotation_fnames = [os.path.join(annotation_dir , f) for f in os.listdir(annotation_dir ) if f.endswith('.ann')]
    annotations = []
    text_ids = set()
    for fname in annotation_fnames:
        text_id = int(os.path.basename(fname).replace('.ann', ''))
        text_ids.add(text_id)
        f = open(fname)
        for line in f:
            annotations.append(BratAnnotation(line, text_id, username))
        f.close()

    db = dbutils.get_database_connection()
    cursor = db.cursor()

    # first, remove all annotations by this (user, text_id) pair
    for text_id in text_ids:
        cursor.execute("SELECT id FROM text_annotations WHERE annotator = '%s' AND text_id = '%d'" % (username, text_id))
        ids = cursor.fetchall()
        for a_id in ids:
            cursor.execute("DELETE FROM text_annotations WHERE id = '%s'" % a_id)
    db.commit()

    for annotation in annotations:
        annotation.insert(cursor)
    db.commit()

    shutil.rmtree(annotation_dir)

def main(args):
    if len(args[1:]) != 1:
        usage = "usage: " + args[0] + " <annotation-directory>\n"
        usage += "* this is the directory that you saved the annotations in\n"

        sys.stderr.write(usage)
        return 1

    annotation_dir = args[1]

    run(annotation_dir)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

