# Stage 1: Build stage
FROM python:3.11-alpine as builder

# Install build dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    sqlite-dev \
    libffi-dev \
    openssl-dev \
    make

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Stage 2: Final stage
FROM python:3.11-alpine

# Install runtime dependencies
RUN apk update && apk add --no-cache \
    libffi \
    openssl \
    sqlite

# Set the working directory
WORKDIR /app

# Copy application files
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Clean up unnecessary files
RUN rm -rf /var/cache/apk/* /root/.cache

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run bot.py when the container launches
CMD ["python3", "bot.py"]
