FROM postgres:13-alpine
ENV POSTGRES_PASSWORD="password123!"
ENV POSTGRES_USER="user"
ENV POSTGRES_DB="database"

RUN mkdir -p /docker-entrypoint-initdb.d
COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432