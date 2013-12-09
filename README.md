# moocdb

## Motivation
Massive Open Online Courses (MOOCs) are becoming an increasingly popular at-a-distance learning option for many students. They're free and available to everyone, and they're huge. Most support a discussion forum where students can reason about course content. These courses also typically feature lectures, readings, assignments, and quizzes / exams. All of this offers a ton of data about the students in the course, something that can be difficult for instructors to get a grasp of. But this also offers a great opportunity for researchers instrested in mining through this data to find connections between participation and learning, dropout rates, subgroup formation, and just about anything else. 

## Goal
How we organize all this data is critically important. This work aims to construct a general, useful, and extensible framework for managing and analyzing all of the data that we might get from a MOOC (and other online communities).

## Getting Started

This is mostly for users who want to play with their own data on their own local machines. 

### Installing MySQL

It's really easy to download MySQL and get it up and running. Head over to their [downloads page](http://dev.mysql.com/downloads/) to get started. The MySQL Community Server page will let you run your own local server if you're into that. If you just want to connect to a remote database, download the MySQL Workbench, which will let you explore the database with a graphical user interface.

### Installing MySQLdb

Since our raw scraped files are in json and csv, we are using python to manipulate them and prepare them for the database. Python is great at manipulating these files, but can't talk directly to MySQL. There are a ton of drivers that link Python to MySQL, but we chose MySQLdb for its transparency. You just have to write SQL code in python and it'll execute for you. While this binds us to MySQL, it lowers the barrier to entry, too. 

You can install MySQLdb from this site: <http://mysql-python.sourceforge.net/MySQLdb.html>

### Exploring the DB with Fake Data!

We've included some scripts to generate fake data for you and insert it into the database. Once you've completed the two steps above, you're ready to create some tables, generate some fake data, and do some db spelunking!

First start by creating the tables in MySQL. Go to the root of this repository and run`./recreate_schema.sh oltp`

Now go into the fakedata folder. Run `./generate_fakedata.py`. This should spew several JSON files full of forum-like data, with heavy plaigarism from War of the Worlds. Finally, run `./populate_db.py` to actually put all this stuff in the database.

If everyone went swimmingly, now it's time to open up your favorite MySQL client and start exploring. As previously mentioned, we recommend MySQL Workbench.

Now you're ready to run some queries! For those, we suggest you hop over to the [wiki](https://github.com/ryanaustincarlson/moocdb/wiki) and check out the [Common Queries page](https://github.com/ryanaustincarlson/moocdb/wiki/common-queries), and if you're unfamiliar with SQL you might take a look at our [cheat sheet](https://github.com/ryanaustincarlson/moocdb/wiki/MySQL-Cheat-Sheet).

