#!/usr/bin/env python

import json, sys
from pprint import pprint

import dbutils

def add_sources(cursor, sources):

    source = sources[0]['name']

    return dbutils.insert_into_table(
            cursor,
            'sources',
            ['name'],
            [source])

def add_forums(cursor, forums, source_id):
    # if an id isn't in forum_ids (if the ordering of the forums is
    # weird) this is going to fail, but for this example we don't need
    # anything too fancy..

    # key=external_id, val=internal_id
    forum_ids = {}
    for forum in forums:
        name = forum['name']
        external_id = forum['forum_id']
        external_parent_id = forum['parent_id']

        cols = ['source_id', 'name', 'external_id']
        vals = [source_id, name, external_id]
        if external_parent_id in forum_ids:
            cols.append('parent_forum_id')
            vals.append(forum_ids[external_parent_id])

        forum_id = dbutils.insert_into_table(
                cursor,
                'forums',
                cols,
                vals)
        
        forum_ids[external_id] = forum_id
                
    return forum_ids

def add_users(cursor, users, source_id):
    # key=external_id, val=internal_id
    user_ids = {}
    for user in users:
        external_id = user['user_id']
        name = user['name']
        registration = user['registered_timestamp']
        last_seen = user['last_seen_timestamp']

        user_id = dbutils.insert_into_table(
                cursor,
                'users',
                ['name'],
                [name])

        user_ids[external_id] = user_id

        dbutils.insert_into_table(
                cursor,
                'user_source',
                ['source_id','user_id','username'],
                [source_id, user_id, external_id])

        dbutils.insert_into_table(
                cursor,
                'user_info',
                ['source_id', 'user_id', 'label', 'value'],
                [source_id, user_id, 'registered_timestamp', registration])

        dbutils.insert_into_table(
                cursor,
                'user_info',
                ['source_id', 'user_id', 'label', 'value'],
                [source_id, user_id, 'last_seen_timestamp', last_seen])

    return user_ids

def add_posts(cursor, posts, source_id, forum_ids, user_ids):
    # if an id isn't in post_ids (if the ordering of the posts is
    # weird) this is going to fail, but for this example we don't need
    # anything too fancy..

    # key=external_id, val=internal_id
    post_ids = {}
    for post in posts:
        external_post_id = post['post_id'] 
        external_user_id = post['user_id'] 
        text = post['text'] 
        timestamp = post['timestamp']
        external_forum_id = post['forum_id'] 
        external_parent_post_id = post['parent_post_id']

        # first deal with texts, so that we can add the text_id field to each
        # post
        text_id = dbutils.insert_into_table(
                cursor,
                'texts',
                ['raw_text'],
                [text])

        # add a "first word" annotation
        dbutils.insert_into_table(
                cursor,
                'text_annotations',
                ['text_id', 'start_pos', 'end_pos', 'annotation_type'],
                [text_id, 0, text.find(' '), 'first_word'])

        cols = ['user_id', 'text_id', 'source_id', 'created_at', 'forum_id']
        vals = [user_ids[external_user_id], text_id, source_id, timestamp, forum_ids[external_forum_id]]

        if external_parent_post_id in post_ids:
            cols.append('parent_post_id')
            vals.append(post_ids[external_parent_post_id])

        post_id = dbutils.insert_into_table(
                cursor,
                'posts',
                cols,
                vals)
        post_ids[external_post_id] = post_id

    return post_ids
        

def main():

    def load_data(fname):
        try:
            with open(fname) as f:
                return json.load(f)
        except:
            sys.stderr.write("Couldn't find \"{}\", did you run ./generate_fakedata?\n".format(fname))
            sys.exit(1)
    sources = load_data('sources.json')
    users = load_data('users.json')
    posts = load_data('posts.json')
    forums = load_data('forums.json')

    db = None
    try:
        db = dbutils.get_database_connection()
        cursor = db.cursor()

        source_id = add_sources(cursor, sources)
        forum_ids = add_forums(cursor, forums, source_id)
        user_ids = add_users(cursor, users, source_id)
        post_ids = add_posts(cursor, posts, source_id, forum_ids, user_ids)
        

        db.commit()   


    finally:
        if db is not None:
            db.close()

if __name__ == '__main__':
    main()

