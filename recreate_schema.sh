#!/usr/bin/env bash

set -u

echo "drop database moocdb" | mysql -u root
echo "create database moocdb" | mysql -u root
mysql -u root -D moocdb < create_oltp_schema_forums.sql

