# Description: Dockerfile for the Python 3.11 image
FROM python:3.11-alpine3.18

# install label studio
RUN pip install label-studio==1.11.0

# copy start.sh to app directory
COPY start.sh /app/start.sh

# set start.sh chmod
RUN chmod +x /app/start.sh

# Set the working directory
WORKDIR /app

# Make port 80 available to the world outside this container
VOLUME /host_directory

# Run app.py when the container launches
CMD ["./start.sh"]