# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install MySQL client library
RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# Set environment variables for MySQL connection
ENV MYSQL_HOST=db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=password
ENV MYSQL_DATABASE=my_database

# Copy the entire project directory into the container
COPY . /app/

# Command to run your Python scripts
CMD ["python", "scripts/analysis.py"]
