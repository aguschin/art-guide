# Use a base Python image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files into the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to run your application when the container starts
CMD ["python", "bot.py"]
