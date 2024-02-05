# Use an official Python runtime as a parent image
FROM python:3.11

# Install specific poetry version to ensure no breaking changes
RUN pip install poetry==1.7.1


# Set environment variables
ENV POETRY_VIRTUALENVS_CREATE=false


# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app


# Install any needed packages specified in requirements.txt
RUN make install

# Make port 8000 available to the world outside this container
EXPOSE 10000

# Run app.py when the container launches
CMD ["make", "run"]