#!/bin/sh
until timeout 10s celery inspect ping; do
  >&2 echo "Celery not available"
done
echo "Starting flower"
celery -A translation_template flower --loglevel=DEBUG
