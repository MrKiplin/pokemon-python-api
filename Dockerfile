# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables for Poetry to manage its virtual environment within the project directory
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
RUN pip install poetry==1.8.2 # Pinning Poetry version for consistency

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock files
# This allows Docker to cache the dependency installation step if these files don't change
COPY pyproject.toml poetry.lock* ./

# Install project dependencies AND the project itself
# Poetry will now create the .venv inside /app due to POETRY_VIRTUALENVS_IN_PROJECT=true
RUN poetry install

# Copy the rest of your application code
COPY . .

# Expose the port your FastAPI application will run on
EXPOSE 8000

# Define the command to run your application using Poetry's script
CMD ["poetry", "run", "start-server"]