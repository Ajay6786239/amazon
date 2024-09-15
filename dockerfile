FROM python:3.11

# Install MySQL development headers and libraries
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    python3-dev \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Set up virtual environment and install Python dependencies
COPY requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application into the container
COPY . /app

# Expose the port and run the application
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mywebsite.wsgi:application"]
