# Asynchronous Text Processing API

This project is a robust, scalable web application built with FastAPI and Celery for asynchronous text processing. It provides a simple REST API to submit text, which is then processed in the background to count words and characters. The application is fully containerized using Docker and Docker Compose for easy setup and deployment.

## Features

-   **RESTful API**: A clean and simple API for submitting tasks and checking their status.
-   **Asynchronous Task Processing**: Utilizes Celery and Redis to handle long-running tasks in the background without blocking the API.
-   **Scalable Architecture**: The separation of the web server and background workers allows for independent scaling.
-   **Containerized**: Fully containerized with Docker and orchestrated with Docker Compose for a consistent and reproducible environment.
-   **Relational Database**: Uses PostgreSQL to persist task information.
-   **Configuration Management**: Centralized configuration using Pydantic's `BaseSettings`.
-   **Data Validation**: Leverages Pydantic for robust request and response data validation.

## Technology Stack

-   **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Task Queue**: [Celery](https://docs.celeryq.dev/en/stable/)
-   **Database**: [PostgreSQL](https://www.postgresql.org/)
-   **Message Broker**: [Redis](https://redis.io/)
-   **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
-   **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
-   **Data Validation & Configuration**: [Pydantic](https://docs.pydantic.dev/)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── config.py       # Application configuration management
│   ├── crud.py         # Database Create, Read, Update, Delete operations
│   ├── database.py     # Database engine and session configuration
│   ├── main.py         # FastAPI application and API endpoints
│   ├── models.py       # SQLAlchemy database models
│   ├── schemas.py      # Pydantic schemas for data validation
│   └── worker.py       # Celery worker and task definitions
├── docker-compose.yml  # Defines and configures all services
├── Dockerfile          # Docker configuration for the API and worker
├── env.template        # Template for environment variables
├── requirements.txt    # Python project dependencies
└── README.md           # This file
```

## Prerequisites

Before you begin, ensure you have the following installed on your system:
-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get the application up and running.

1.  **Clone the repository** (if you haven't already):
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create the environment configuration file**:
    Copy the template to a new `.env` file. This file contains the necessary environment variables for the database and other services.
    ```sh
    cp env.template .env
    ```
    You can modify the values in `.env` if needed, but the defaults are configured to work with Docker Compose.

3.  **Build and run the services**:
    Use Docker Compose to build the images and start all the containers (API, worker, PostgreSQL, and Redis) in detached mode.
    ```sh
    docker-compose up -d --build
    ```
    The API will be available at `http://localhost:8000`.

## API Documentation

### 1. Create a new analysis task

Submits a new text for analysis. The task is added to a queue for background processing.

-   **URL**: `/api/tasks`
-   **Method**: `POST`
-   **Status Code**: `202 Accepted`
-   **Request Body**:

    ```json
    {
      "text": "This is a sample text for analysis."
    }
    ```

-   **Success Response**:
    The response includes the `task_id` which can be used to check the status of the task.

    ```json
    {
      "task_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
    }
    ```

### 2. Get task status and result

Retrieves the status and result of a specific task using its ID.

-   **URL**: `/api/tasks/{task_id}`
-   **Method**: `GET`
-   **URL Params**:
    -   `task_id=[uuid]` (Required) - The ID of the task to retrieve.

-   **Success Responses**:

    -   **If the task is still pending or in progress**:

        ```json
        {
          "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
          "status": "PENDING",
          "result": null
        }
        ```

    -   **If the task is completed**:
        The `result` field will contain the analysis output.

        ```json
        {
          "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
          "status": "COMPLETED",
          "result": {
            "word_count": 7,
            "char_count": 35
          }
        }
        ```

-   **Error Response**:

    -   **If the task is not found**:
        -   **Status Code**: `404 Not Found`
        -   **Response Body**:
            ```json
            {
              "detail": "Task not found"
            }
            ```

## Application Workflow

1.  A client sends a `POST` request with text to the `/api/tasks` endpoint.
2.  The **FastAPI application** validates the input, creates a new task record in the **PostgreSQL** database with a `PENDING` status, and returns a `task_id`.
3.  The API then enqueues a new job in the **Celery** task queue via the **Redis** message broker.
4.  A **Celery worker** picks up the job from the queue.
5.  The worker updates the task status to `IN_PROGRESS`, performs the text analysis (simulated with a delay), and updates the task record in the database with the `COMPLETED` status and the analysis result.
6.  The client can poll the `/api/tasks/{task_id}` endpoint to check the status and retrieve the result once the task is complete.

## Managing the Application

-   **Start the application**:
    ```sh
    docker-compose up -d
    ```

-   **Stop the application**:
    ```sh
    docker-compose down
    ```

-   **View logs**:
    ```sh
    # View logs for all services
    docker-compose logs -f

    # View logs for a specific service (e.g., the api)
    docker-compose logs -f api
    ```
