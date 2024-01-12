# Use an official Python runtime as a base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#make dir
RUN mkdir /code

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /app
COPY . /code/

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     libpq-dev \
#     gcc \
#     # any other dependencies
#     && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run your app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]