FROM python:3.9-alpine3.13

# Label to mark the maintainer of the image
LABEL maintainer="ErmiasBrhane"

# Ensures Python output is not buffered, making logs easier to read
ENV PYTHONUNBUFFERED 1

# Copy the requirements files to the container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the application code into the container
COPY ./app /app

# Set the working directory inside the container
WORKDIR /app

# Expose port 8000 to allow external access
EXPOSE 8000

# Argument to determine if we want to install development dependencies
ARG DEV=false

# Install dependencies and create the virtual environment
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Install dev dependencies if the DEV argument is true
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp && \
    # Add a non-root user to the container
    adduser --disabled-password --no-create-home --gecos "" django-user

# Set the PATH environment variable to include the virtual environment's bin directory
ENV PATH="/py/bin:$PATH"

# Switch to the non-root user for security reasons
USER django-user

