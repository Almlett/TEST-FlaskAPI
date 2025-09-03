# This Dockerfile defines the environment for running a Python web application.
# It creates a containerized version of the application, ensuring a consistent
# and reproducible runtime environment.

# Specifies the base image for the container.
# 'python:3.10-slim' is a lightweight version of the official Python 3.10 image,
# which helps in keeping the final image size small.
FROM python:3.10-slim

# Sets the working directory inside the container to '/app'.
# All subsequent commands (like COPY, RUN, CMD) will be executed from this path.
WORKDIR /app

# Copies the Python dependencies file from the host machine to the container's
# working directory. This is done as a separate step to leverage Docker's layer
# caching. If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .

# Installs the Python packages listed in requirements.txt using pip.
# The '--no-cache-dir' flag is used to prevent pip from storing the package
# cache, which further reduces the final image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copies the rest of the application's source code from the current directory
# on the host machine into the container's working directory ('/app').
COPY . .

# Sets the PYTHONPATH environment variable to the application's root directory.
# This ensures that Python can find the application's modules and packages
# without needing relative imports.
ENV PYTHONPATH=/app

# Defines the default command to execute when the container starts.
# It runs the application using the 'uvicorn' ASGI server.
# - 'app.main:app': Specifies the application instance to run (the 'app' object in the 'app/main.py' file).
# - '--host 0.0.0.0': Binds the server to all available network interfaces, making it accessible from outside the container.
# - '--port 8000': Exposes the application on port 8000 inside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
