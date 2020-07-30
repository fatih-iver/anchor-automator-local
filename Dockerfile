# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8.5

# Make print()'s to be seen immediately
ENV PYTHONUNBUFFERED 1

# Install Chrome v(84.0.4147.105-1)
COPY google-chrome-v84.0.4147.105-1_amd64.deb google-chrome-v84.0.4147.105-1_amd64.deb
RUN dpkg -i google-chrome-v84.0.4147.105-1_amd64.deb; apt-get update -y; apt-get -fy install

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application file
COPY main.py main.py

# Start execution
ENTRYPOINT ["python", "main.py"]
