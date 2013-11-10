
-- Sources Coursera, FB, Quora, Twitter etc.
create table sources (
  id serial primary key,
  name text
);

-- Primary Users table
create table users (
  id serial primary key,
  name text,
  age int,
  gender int,
  website1 text
);

-- Links User to source and stores basic connection information 
-- such as user handle etc.
create table user_source (
  id serial primary key,
  source_id int references sources(id),
  user_id int references users(id),
  username text
);

-- User data from various sources
create table user_info (
  id serial primary key,
  source_id int references sources(id),
  user_id int references users(id),
  key text,
  value text
);

-- Hierarchial categorization in terms of forums.
create table forums (
  id serial primary key,
  parent_forum_id int references forums(id),
  name text
);

-- List of raw texts in Unicode
create table texts (
  id serial primary key,
  raw_text text
);

-- Various annotations on the text.
-- More discussion required. Could be extended to be heirarchical, or
-- include XML/JSON structures.
create table text_annotations (
  id serial primary key,
  text_id int references texts(id),
  start_pos int,
  end_pos int,
  annotation_type text
);

-- Could have a separate table for links if the
-- analysis was needed.

create table threads (
  id serial primary key,
  user_id int references users(id),
  -- Might not necessarily be attached to a forum.
  forum_id int references forums(id),
  text_id int references texts(id),
  created_at timestamp,
  updated_at timestamp
);

create table thread_tags (
  id serial primary key,
  thread_id int references threads(id),
  tag1 text,
  tag2 text,
  tag3 text
);

-- Posts table. Most important table. Contains user posts.
-- Could be Coursera questions, tweets, FB comments.
create table posts (
  id serial primary key,
  -- Doesn't always have to have a thread, for instance twitter.
  thread_id int references threads(id),
  created_user_id int references users(id),
  parent_post_id int references posts(id),
  text_id int references texts(id),
  created_at timestamp,
  updated_at timestamp
);

-- List of users the post refers to.
create table post_user_references (
  id serial primary key,
  post_id int references posts(id),
  user_id int references users(id)
);

create table post_votes (
  id serial primary key,
  post_id int references posts(id),
  user_id int references users(id),
  vote int,
  created_at timestamp
);






