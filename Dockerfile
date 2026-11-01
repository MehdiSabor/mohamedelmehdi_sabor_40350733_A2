# Start from Ubuntu 24.04 (like the lab's Nginx exercise)
FROM ubuntu:24.04

# Install Python and the libraries the code uses
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python-is-python3
RUN apt-get install -y python3-pandas
RUN apt-get install -y python3-dotenv

# Install MPI (Open MPI gives the mpirun command, mpi4py lets Python use it)
RUN apt-get install -y openmpi-bin
RUN apt-get install -y python3-mpi4py

# Install SSH (mpirun uses it to start Python on the other containers)
RUN apt-get install -y openssh-server
RUN apt-get install -y openssh-client

# Create a normal user (Open MPI refuses to run as root)
RUN useradd -m -s /bin/bash mpiuser

# Folder the SSH server needs to start
RUN mkdir -p /run/sshd

# Create one SSH key and trust it, so containers log into each other without a password
USER mpiuser
RUN mkdir -p /home/mpiuser/.ssh
RUN ssh-keygen -t rsa -N "" -f /home/mpiuser/.ssh/id_rsa
RUN cp /home/mpiuser/.ssh/id_rsa.pub /home/mpiuser/.ssh/authorized_keys
RUN echo "StrictHostKeyChecking no" > /home/mpiuser/.ssh/config
RUN echo "UserKnownHostsFile /dev/null" >> /home/mpiuser/.ssh/config
RUN echo "LogLevel ERROR" >> /home/mpiuser/.ssh/config
RUN chmod 700 /home/mpiuser/.ssh
RUN chmod 600 /home/mpiuser/.ssh/id_rsa
RUN chmod 600 /home/mpiuser/.ssh/authorized_keys
RUN chmod 600 /home/mpiuser/.ssh/config
USER root

# Copy the project code into /app (the dataset is not copied, it is given to the master at run time)
COPY . /app
WORKDIR /app

# Where the dataset will be inside the master container (workers get their rows from the master)
ENV PATH_DATASET=/data/Books_rating.csv

# SSH port, so the containers can reach each other
EXPOSE 22/tcp

# Keep the SSH server running, which keeps the container alive
CMD ["/usr/sbin/sshd", "-D"]
