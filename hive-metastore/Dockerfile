FROM apache/hive:4.0.0

USER root

ADD https://jdbc.postgresql.org/download/postgresql-42.7.3.jar /opt/hive/lib/postgres.jar
RUN chmod 644 /opt/hive/lib/postgres.jar

USER hive
