# Use a slim Python image for smaller size
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for psycopg2-binary
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies needed for the entrypoint script
RUN apk add --no-cache netcat-openbsd

# Copy requirements.txt and install Python dependencies
# This step is done separately to leverage Docker caching,
# so dependencies are only reinstalled if requirements.txt changes.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the port your Django application will run on
EXPOSE 8000

# Run collectstatic to gather all static files
# CMD should be used instead of RUN for commands that run when the container starts
# For collectstatic, it's typically done as a build step or during entrypoint
# Let's add it to the entrypoint script for robustness
# Or you can run it manually on first build after migrations
# For simplicity in this base Dockerfile, we'll assume collectstatic is run
# as part of an entrypoint script or manually if static files are served by Nginx later.
# For now, we'll keep the CMD simple to start Gunicorn.

# Copy the entrypoint script into the container
COPY ./entrypoint.sh /app/entrypoint.sh
# Make it executable inside the container
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Define the command to run the Gunicorn server
# Make sure to bind to 0.0.0.0 for container networking
# Use your main project's wsgi.py
CMD ["gunicorn", "pythonnetworkmonitor.wsgi:application", "--bind", "0.0.0.0:8000"]
