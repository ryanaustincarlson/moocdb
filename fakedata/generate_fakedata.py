#!/usr/bin/env python

import sys, random
import datetime, calendar
import csv
try:
    import json
except:
    import simplejson as json
from pprint import pprint

NUM_USERS = 5
MAX_NUM_POSTS = 5

random.seed(10) # NOTE: means we'll get the same psedo-random list each time

def get_names():
    baby_file = open('baby-names.csv', 'r')
    names = set()

    reader = csv.reader(baby_file)
    header = reader.next()
    for year, name, percent, gender in reader:
        names.add(name)
    baby_file.close()
    namelist = list(names)

    random.shuffle(namelist)

    return iter(namelist)

def get_user_ids():
    ids = range(1,NUM_USERS * 100)
    random.shuffle(ids)
    return iter(ids)

def get_registration_timestamps():
    times = range(1, NUM_USERS * 10)
    random.shuffle(times)
    return iter(times)

def get_last_seen_timestamps():
    times = range(NUM_USERS * 1000, NUM_USERS * 2000)
    random.shuffle(times)
    return iter(times)

def get_post_ids():
    ids = range(NUM_USERS * MAX_NUM_POSTS * 10)
    random.shuffle(ids)
    return iter(ids)

def get_words():
    # read from The War of the Worlds
    f = open('war-of-the-worlds.txt', 'r') 
    book = f.read()
    f.close()
    words = book.split()

    snippets = []

    increment = 10
    index = increment
    for index in range(0, len(words), increment):
        snippets.append(' '.join(words[index:index+increment]))

    random.shuffle(snippets)
    return iter(snippets)

def get_forums():
    def construct_forum(name, uid, parent_uid):
        return {'name':name, 'forum_id':uid, 'parent_id':parent_uid}
    forums = []
    forums.append(construct_forum('Week 1', 10, None))
    forums.append(construct_forum('Discussion of Invasian', 20, 10))
    forums.append(construct_forum('Discussion of Humans', 30, 10))
    forums.append(construct_forum('Alien Symbolism', 40, 20))
    return forums

def main():
    # get some iterators
    names = get_names()
    user_ids = get_user_ids()
    registrations = get_registration_timestamps()
    last_seens = get_last_seen_timestamps()
    post_ids = get_post_ids()
    words = get_words()

    sources = [{'name':'War of the Worlds'}]

    # get some users
    users = []
    for i in xrange(NUM_USERS):
        user = {}
        user['name'] = names.next()
        user['user_id'] = user_ids.next()
        user['registered_timestamp'] = registrations.next()
        user['last_seen_timestamp'] = last_seens.next()

        users.append(user)
    user_ids = [user['user_id'] for user in users]

    forums = get_forums()
    thread_id = forums[-1]['forum_id']

    # get some posts by those users
    posts = []
    is_first_user = True
    parent_post = None

    for user_id in user_ids:
        num_posts = random.randint(1, MAX_NUM_POSTS)
        is_first_post = True
        for post in range(num_posts):
            post = {}
            post['post_id'] = post_ids.next()
            post['user_id'] = user_id
            post['text'] = words.next()
            post['forum_id'] = thread_id

            last_timestamp = posts[-1]['timestamp'] if len(posts) > 0 else 100
            post['timestamp'] = last_timestamp + random.randint(20, 50)

            this_parent = None
            if is_first_post:
                if is_first_user:
                    parent_post = post['post_id']
                else:
                    this_parent = parent_post
            post['parent_post_id'] = this_parent

            posts.append(post)

            is_first_post = False
        is_first_user = False


    def write_data(json_obj, fname):
        f = open(fname, 'w') 
        json.dump(json_obj, f, indent=2)
        f.close()
        sys.stderr.write('wrote ' + fname + '\n')

    write_data(sources, 'sources.json')
    write_data(users, 'users.json')
    write_data(posts, 'posts.json')
    write_data(forums, 'forums.json')

if __name__ == '__main__':
    main()

