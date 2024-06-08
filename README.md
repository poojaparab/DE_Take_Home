# AWS SQS to POstgresSQL

## Overview

This project demonstrates a small application that reads user login behavior data from an AWS SQS Queue, masks personal identifiable information (PII), and writes the transformed data to a PostgreSQL database. The entire process runs locally using Docker containers.

## Components

### Docker Compose

The `docker-compose.yml` file defines the services required for this project:
- **localstack**: Simulates AWS services locally.
- **postgres**: Runs a PostgreSQL database with pre-created tables.
- **fastapi-app**: The main application service that reads from SQS, masks data, and writes to PostgreSQL.

### FastAPI Application

The main application (`main.py`) includes:
- **Endpoints**:
  - `GET /`: Returns a greeting message.
  - `GET /read-messages`: Reads messages from SQS and returns them.
  - `GET /write-messages`: Reads messages from SQS, masks the data, and writes it to PostgreSQL.

- **Functions**:
  - `read_messages()`: Reads messages from the SQS queue.
  - `write_to_postgres(records: List[Record])`: Writes the masked records to PostgreSQL.

### Utilities

The `utils.py` file includes utility functions for data transformation:
- **mask_value(value)**: Masks a given value using SHA-256 hashing.
- **mask_data(record)**: Masks the `ip` and `device_id` fields in the record.
- **convert_app_version(app_version)**: Converts app version string to a numerical format.

### Dockerfile

The `Dockerfile-webapp` sets up the FastAPI application environment:
- **Base Image**: `python:3.9-slim`
- **Working Directory**: `/app`
- **Dependencies**: Installed from `requirements.txt`
- **Application Code**: Copied into the container
- **Command**: Runs the FastAPI application using `uvicorn`

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Start the Docker Services**:

    ```bash
    docker-compose up

3. **Access the FastAPI Application**:
    Open your browser and navigate to http://localhost:8000 to access the API endpoints.

## API Endpoints
- GET /: Simple greeting message.
- GET /read-messages: Reads and returns messages from the SQS queue.
- GET /write-messages: Reads messages from SQS, masks PII fields, and writes to       PostgreSQL.

## Notes
- Ensure Docker is installed and running on your machine.
- The SQS queue and PostgreSQL database are simulated locally using Localstack and a custom PostgreSQL image.
- The FastAPI application uses placeholder AWS credentials for Localstack.

## Contact
For any issues or questions, please contact [poojaparab9035@gmail.com].

