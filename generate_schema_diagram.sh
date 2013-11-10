
# Should change the hard coded db/user names to environment variables.

java -jar schemaSpy.jar -t pgsql -db library -host localhost -u pulkit -s public -db moocdb -port 5432 -o library -dp postgresql-9.3-1100.jdbc3.jar

