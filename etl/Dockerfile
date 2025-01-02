# Start with the official Postgres image
FROM postgres:15

# Create a working directory for your scripts
WORKDIR /healthdashboard/etl

# Copy migration files and ETL scripts into the container
COPY . .

# Install Python (required for ETL script)
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir -r /app/etl/requirements.txt

# Add a script to initialize the database (migrations and ETL)
COPY init-db.sh /docker-entrypoint-initdb.d/

# Expose the default Postgres port
EXPOSE 5432