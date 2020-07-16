# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8.4

# Make print()'s to be seen immediately
ENV PYTHONUNBUFFERED 1

# Install Chrome (v84.0.4147.89-1)
COPY google-chrome-stable_84.0.4147.89-1_amd64.deb google-chrome-stable_84.0.4147.89-1_amd64.deb
RUN dpkg -i google-chrome-stable_84.0.4147.89-1_amd64.deb; apt-get update -y; apt-get -fy install

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application file
COPY main.py main.py

# Start execution
ENTRYPOINT ["python", "main.py"]
