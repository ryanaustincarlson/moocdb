#!/usr/bin/env bash

usage() {
  echo -e 'Drops the DB and recreates the schema.'
  echo -e 'Usage:'
  echo -e 'script [ oltp | olap ]'
}

recreate_oltp() {
  echo "drop database moocdb" | mysql
  echo "create database moocdb" | mysql
  mysql -D moocdb < create_oltp_schema_forums.sql
}

recreate_olap() {
  echo "drop database moocdb_olap" | mysql
  echo "create database moocdb_olap" | mysql
  mysql -D moocdb_olap < create_olap_star_schema_forums.sql
}

if [ "$#" -ne 1 ]; then
  usage
  exit 1
fi

case "$1" in
  "oltp" )
    recreate_oltp
    ;;
  "olap" )
    recreate_olap
    ;;
  * )
    usage
    ;;
esac

