# Use a base Python image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

COPY requirements.txt /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the necessary files into the container
COPY . /app

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Command to run your application when the container starts
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
