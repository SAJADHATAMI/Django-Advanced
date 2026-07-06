### Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY ./blogsite/requirements.txt /app/
# update and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

### copy the current directory contents into the container at /app
COPY ./blogsite /app/
