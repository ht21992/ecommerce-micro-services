#!/bin/sh
# /app/entrypoint.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Define variables for clarity and easy modification
MAX_RETRIES=30
SLEEP_SECONDS=2
COUNTER=0

# Use Django's built-in 'check' command for a lightweight and reliable DB check
echo "Waiting for database connection..."
until python manage.py check --database default > /dev/null 2>&1 || [ $COUNTER -ge $MAX_RETRIES ]; do
  COUNTER=$((COUNTER+1))
  echo "Database unavailable, waiting $SLEEP_SECONDS seconds... (Attempt: $COUNTER/$MAX_RETRIES)"
  sleep $SLEEP_SECONDS
done

# Exit if the database is still not available after all retries
if [ $COUNTER -ge $MAX_RETRIES ]; then
  echo "Error: Database connection failed after $MAX_RETRIES retries."
  exit 1
fi

echo "✅ Database is ready."

# Make Migrations
echo "making migrations..."
python manage.py makemigrations


# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Optional: collect static files
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start the server using 'exec'.
# This makes the server process the main process (PID 1),
# allowing it to receive signals correctly for graceful shutdowns.
echo "🚀 Starting server..."
exec python manage.py runserver 0.0.0.0:8000