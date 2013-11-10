
usage() {
  echo -e 'Drops the DB and recreates the schema.'
  echo -e 'Usage:'
  echo -e 'script [ oltp | olap ]'
}

recreate_oltp() {
  dropdb moocdb
  createdb moocdb
  psql -d moocdb < create_oltp_schema_forums.sql
}

recreate_olap() {
  dropdb moocdb_olap
  createdb moocdb_olap
  psql -d moocdb_olap < create_olap_star_schema_forums.sql
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

