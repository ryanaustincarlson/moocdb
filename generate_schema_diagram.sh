
# TODO: Should change the hard coded db/user names to environment variables.

java -jar schemaSpy.jar -t pgsql -o schema/oltp -host localhost -u $USER -s public -db moocdb -port 5432 -dp postgresql-9.3-1100.jdbc3.jar

