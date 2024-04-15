FROM python:3.9 AS database_servicio
# Install system dependencies and Ansible
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common ansible sshpass  ssh-askpass openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Create a dedicated user for running the application
RUN useradd -u 1000 -ms /bin/bash db_demo
RUN mkdir -p /home/db_demo/inventory/
RUN mkdir -p /home/db_demo/app/group_vars/
# Set the working directory
WORKDIR /home/db_demo/app/

# Copy requirements files separately to leverage Docker's layer caching
COPY requirements.txt /home/db_demo/app/requirements.txt
COPY requirements.yml /home/db_demo/app/requirements.yml



# Install Python dependencies and Ansible roles
RUN pip install -r requirements.txt && \
    ansible-galaxy install -r requirements.yml

# Copy the application code
COPY . /home/db_demo/app/

# Set ownership to the db_demo user
RUN chown -R db_demo:db_demo /home/db_demo/app/

# Stage 2: Testing environment
FROM database_servicio AS testing

# Switch to the db_demo user
USER db_demo

RUN mkdir /home/db_demo/.ssh/ && \
    ssh-keygen -t rsa -N "" -f /home/db_demo/.ssh/id_rsa


# Expose the port your application listens on
EXPOSE 5000

# Define the command to run your application
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
