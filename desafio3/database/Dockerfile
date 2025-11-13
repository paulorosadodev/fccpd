FROM postgres:16-alpine

ENV POSTGRES_DB=battle_arena
ENV POSTGRES_USER=arena_master
ENV POSTGRES_PASSWORD=battle123

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
