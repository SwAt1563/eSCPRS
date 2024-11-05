# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define build-time arguments for user and group
ARG GROUP_ID=1001
ARG USER_ID=1001
ARG GROUP_NAME=sight
ARG USER_NAME=qutaiba
ARG APP_DIR=/app

# Create a group and user with specified IDs and names
RUN groupadd -g ${GROUP_ID} ${GROUP_NAME} && \
    useradd -u ${USER_ID} -g ${GROUP_NAME} -m ${USER_NAME}

# Install necessary build and runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \ 
    curl \
    gnupg \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    gettext \
    # Makefile
    make \
    # For VectorStore 
    cmake \
    build-essential \ 
    libopenblas-dev \
    libomp-dev \
    libblas-dev \
    && rm -rf /var/lib/apt/lists/*



# Set up the application directory
WORKDIR ${APP_DIR}

# Copy the application code to the /app directory
COPY . ${APP_DIR} 

# Ensure executable permissions for the scripts
# Don't forget to remove volumes from the docker-compose file
RUN chmod +x ${APP_DIR}/start_server.sh 


# Ensure correct permissions
RUN chmod -R 755 ${APP_DIR}


# Set permissions
# to make it work you need to stop the '/app' volume in the docker-compose file
# handle static files in github actions
RUN chown -R ${USER_NAME}:${GROUP_NAME} ${APP_DIR} 


# Switch to the new user
USER ${USER_NAME}



# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip --no-cache-dir

# Install Python packages
RUN pip install -r requirements.txt --no-cache-dir


