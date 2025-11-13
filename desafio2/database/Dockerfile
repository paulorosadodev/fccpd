FROM postgres:16-alpine

ENV POSTGRES_DB=tavern_rpg
ENV POSTGRES_USER=gamemaster
ENV POSTGRES_PASSWORD=hero123

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
