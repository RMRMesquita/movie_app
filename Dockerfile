# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Set environment variable for Flask app
ENV FLASK_APP=app.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application using Flask CLI for development or uncomment for production
# Comment for production
CMD ["flask", "run"]
# Uncomment for production
# CMD ["python", "app.py"]
