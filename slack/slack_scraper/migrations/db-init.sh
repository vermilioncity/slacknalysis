#!/bin/sh

for f in /home/views/*
  do
    echo "Creating view from $f..."
    filename=$(basename $f)
    filename="${filename%.*}"
    psql -U slacker -d slacknalysis -c "DROP VIEW ${filename} CASCADE;"
    psql -U slacker -d slacknalysis -f "/home/views/${filename}.sql"
  done
