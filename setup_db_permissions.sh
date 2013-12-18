#!/bin/bash

for table in `echo "SELECT schemaname || '.' || relname FROM pg_stat_user_tables;" | psql moocdb | grep "^ " | grep -v "?column"`
do
    cmd="GRANT ALL ON TABLE $table TO PUBLIC;"
    echo -n "$cmd ... "
    echo "$cmd" | psql moocdb
done

for sequence in `echo "SELECT schemaname || '.' || relname FROM pg_statio_all_sequences;" | psql moocdb | grep "^ " | grep -v "?column"`
do
    cmd="GRANT ALL ON SEQUENCE $sequence TO PUBLIC;"
    echo -n "$cmd ... "
    echo "$cmd" | psql moocdb
done
