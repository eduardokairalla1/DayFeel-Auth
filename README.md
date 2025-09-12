# Dayfeel_auth

This is a service to take care of DayFeel API authentications

-----

## 🚀 Getting Started (Local Development)

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites

  * **Python** 3.9+
  * **Poetry** for dependency management
  * **Docker** for containerization

### 2. Initial Configuration

First, set up your local environment variables by copying the example file:

```bash
cp .env.example .env
```

Now, open the `.env` file and customize the variables for your environment.

> **Important:** Remember to also add any new environment variables to the configuration model in the `models.py` file.

### 3. Install Dependencies

Use Poetry to install all necessary Python packages. This command reads the `pyproject.toml` file and creates a virtual environment for you.

```bash
poetry install
```

### 4. Run the Application

To run the development server, you can use `poetry run` to execute the script within the correct virtual environment:

```bash
poetry run scripts/dev
```

Alternatively, you can activate the virtual environment first with `poetry shell` and then run the script directly.

The API should now be running on the specified host and port (e.g., `http://0.0.0.0:8000`).

-----

## 📚 Using the API

Once the application is running, you can access the interactive API documentation (powered by Swagger UI) in your browser:

➡️ **[http://localhost:8000/docs](http://localhost:8000/docs)**

This interface allows you to explore all available endpoints, view their parameters, and test them live.

-----

## 🧪 Running Tests

To run the full suite of automated tests, use the following command:

```bash
poetry run scripts/test
```

-----

## 🐳 Deploying with Docker

This project is designed to be deployed as a Docker container.

### Building the Image

To build the Docker image, run the `build` script with your Docker Hub username:

```bash
DOCKER_USER=your-docker-hub-user scripts/build
```

This will build and tag the image (e.g., `your-docker-hub-user/dayfeel_auth:0.0.1`).

> **Note:** The production Docker image exposes the application on port **80**, while the local development server (`scripts/dev`) runs on port **8000**.

-----

## ❤️ Health Check

The application includes a health check endpoint to monitor its status. You can query it using `curl`:

```bash
# Example for a locally running instance
curl -fsS http://localhost:8000/health | jq .
```
