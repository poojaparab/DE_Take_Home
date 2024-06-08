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

## Questions

1. **How would you deploy this application in production?**
    - Deploy the FastAPI application to a cloud provider like AWS, Azure, or Google Cloud Platform using their respective services for containers (e.g., ECS, AKS, GKE).
    - Set up a managed PostgreSQL database service for production use.
    - Use AWS SQS or a similar queue service (apache kafka, pubsub) in the chosen cloud provider for message queuing.

2. **What other components would you want to add to make this production ready?**
    - Implement proper logging mechanisms to track application behavior and errors.
    - Set up monitoring and alerting for application metrics and health checks.
    - Implement security measures such as encryption for data in transit and at rest.
    - Add authentication and authorization mechanisms to secure access to the application and its endpoints.
    - creating configuration files for different environments which includes all the environment variables.

3. **How can this application scale with a growing dataset?**
    - Utilize auto-scaling capabilities of container orchestration platforms to dynamically adjust resources based on demand.
    - Implement sharding or partitioning strategies for the database to distribute data across multiple nodes.
    - Use distributed queue systems for handling larger volumes of messages efficiently.

4. **How can PII be recovered later on?**
    - Using hashlib.sha256 irreversibly hashes the PII data, meaning that once it's hashed, it cannot be recovered to its original form. Therefore, if you're using hashlib.sha256 to mask PII data, you won't be able to recover it later.

    - If you need to recover PII data later on, you would need to use encryption rather than hashing. Encryption allows for reversible transformation of data, meaning you can encrypt the PII data and then decrypt it later when needed.

    - Alternatives to hashlib.sha256 for masking PII data include:
        1. Encryption algorithms: AES and RSA
        2. Tokenization: Replace sensitive data with randomly generated tokens or pseudonyms
        3. AWS and GCP also provides like KMS to encrypt data at rest.

5. **What are the assumptions you made?**
    - The application assumes that the incoming data from the SQS queue is in JSON format and follows a specific structure.
    - It assumes that the provided Docker images for local development accurately replicate the behavior of AWS SQS and PostgreSQL.


## Notes
- Ensure Docker is installed and running on your machine.
- The SQS queue and PostgreSQL database are simulated locally using Localstack and a custom PostgreSQL image.
- The FastAPI application uses placeholder AWS credentials for Localstack.

## Contact
For any issues or questions, please contact [poojaparab9035@gmail.com].

