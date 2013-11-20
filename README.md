# moocdb

## Motivation
Massive Open Online Courses (MOOCs) are becoming an increasingly popular at-a-distance learning option for many students. They're free and available to everyone, and they're huge. Most support a discussion forum where students can reason about course content. These courses also typically feature lectures, readings, assignments, and quizzes / exams. All of this offers a ton of data about the students in the course, something that can be difficult for instructors to get a grasp of. But this also offers a great opportunity for researchers instrested in mining through this data to find connections between participation and learning, dropout rates, subgroup formation, and just about anything else. 

## Goal
How we organize all this data is critically important. This work aims to construct a general, useful, and extensible framework for managing and analyzing all of the data that we might get from a MOOC (and other online communities).

## Getting Started

### Installing PG8000

Since our raw scraped files are in json and csv, we are using python to manipulate them and prepare them for the database. Python is great at manipulating these files, but can't talk directly to Postgres. There are a ton of drivers that link Python to Postgres, but we chose PG8000 for its transparency. You just have to write SQL code in python and it'll execute for you. While this binds us to Postgres, it lowers the barrier to entry, too. 

You can install PG8000 with pip: `pip install pg8000`.
