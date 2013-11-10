
# TODO: Should change the hard coded db/user names to environment variables.

usage() {
  echo -e 'Generates the schema diagram.'
  echo -e 'Usage:'
  echo -e 'script [ oltp | olap ]'
}

generate_oltp() {
  java -jar schemaSpy.jar -t pgsql -o schema/oltp -host localhost -u pulkit -s public -db moocdb -port 5432 -dp postgresql-9.3-1100.jdbc3.jar
}

generate_olap() {
  java -jar schemaSpy.jar -t pgsql -o schema/olap -host localhost -u pulkit -s public -db moocdb_olap -port 5432 -dp postgresql-9.3-1100.jdbc3.jar
}

if [ "$#" -ne 1 ]; then
  usage
  exit 1
fi

case "$1" in
  "oltp" )
    generate_oltp
    ;;
  "olap" )
    generate_olap
    ;;
  * )
    usage
    ;;
esac


