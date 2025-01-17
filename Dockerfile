# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Install necessary packages and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    wget \
    curl \
    libpq-dev \
    postgresql-server-dev-all \
    libicu-dev \
    liblz4-dev \
    libzstd-dev \
    libreadline-dev \
    libssl-dev \
    libldap2-dev

# Set the working directory
WORKDIR /usr/src/app

# Clone the pgvector repository
RUN git clone https://github.com/pgvector/pgvector.git

# Change to the pgvector directory
WORKDIR /usr/src/app/pgvector

# Build the pgvector extension
RUN make && make install

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

# Expose the default PostgreSQL port
EXPOSE 5432

# Start PostgreSQL
CMD ["postgres"]
