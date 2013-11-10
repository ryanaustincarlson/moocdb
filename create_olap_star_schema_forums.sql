
-- source_dimension Coursera, FB, Quora, Twitter etc.
create table source_dimension (
  id serial primary key,
  name text
);

-- Primary Users table
create table user_dimension (
  id serial primary key,
  name text,
  age int,
  gender int,
  website1 text
);

create table time_dimension (
  id serial primary key,
  year int,
  month int,
  week int,
  day int,
  hour int
);

create table location_dimension (
  id serial primary key,
  country text,
  state text,
  city text,
  pincode int,
  lattitude double precision,
  longitude double precision
);

create table forums (
  id serial primary key,
  parent_forum_id int references forums(id),
  source_id int references source_dimension(id),
  name text
);

create table user_data_measure (
  id serial primary key,
  source_id int references source_dimension(id),
  time_id int references time_dimension(id),
  user_id int references user_dimension(id),
  key text,
  value text
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

-- Posts table. Most important table. Contains user posts.
-- Could be Coursera questions, tweets, FB comments.
create table posts_measure (
  id serial primary key,
  -- May be a thread starter post.
  typeof int,
  user_id int references user_dimension(id),
  parent_post_user_id int references user_dimension(id),
  -- Assuming only 1 referenced user. Leaving out multiple references
  -- for the sake of simplicity.
  referenced_user_id int references user_dimension(id),
  parent_post_id int references posts_measure(id),
  source_id int references source_dimension(id),
  time_id int references time_dimension(id),
  location_id int references location_dimension(id),
  text_id int references texts(id),
  forum_id int references forums(id)
);

create table post_votes_measure (
  id serial primary key,
  post_id int references posts_measure(id),
  user_id int references user_dimension(id),
  time_id int references time_dimension(id),
  location_id int references location_dimension(id),
  vote int
);



