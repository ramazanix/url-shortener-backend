#!/bin/sh

# Apply migrations
sleep 5
alembic upgrade head
exec "$@"
