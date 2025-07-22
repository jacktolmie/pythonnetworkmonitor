#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# These variables (DB_HOST, DB_PORT) will come from docker-compose.yml
DB_HOST=${DB_HOST:-db-1}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for postgres at $DB_HOST:$DB_PORT..."

# We use a loop with netcat (nc) to check if the port is open.
# The postgres container might be running but not ready to accept connections.
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

# Now that the database is ready, run the migrations.
echo "Running database migrations..."
python manage.py migrate

# Now start the Gunicorn server.
# The `exec "$@"` is important to ensure Gunicorn receives signals correctly.
echo "Starting Gunicorn server..."
exec "$@"
