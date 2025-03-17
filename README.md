# Receipt Processor

A simple receipt processor webservice that fulfills the documented API. This API allows you to process receipts and calculate points based on various criteria. This is my submission for the Receipt Processor Challenge by Fetch Rewards.

## Features

- Process receipts and calculate points
- Retrieve points for a specific receipt
- Input validation using Pydantic models

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/shreyamtaneja/fetch.git
    cd fetch
    ```

## Running the Application with Docker

1. Build the Docker image:

    ```bash
    docker build -t fetch .
    ```

2. Run the Docker container:

    ```bash
    docker run --name fastserver -p 80:80 fetch
    ```

3. The API will be available at `http://0.0.0.0:80`.

## API Endpoints

### Process Receipt

- **URL**: `/receipts/process`
- **Method**: `POST`
- **Request Body**:

    ```json
    {
        "retailer": "string",
        "purchaseDate": "YYYY-MM-DD",
        "purchaseTime": "HH:MM",
        "items": [
            {
                "shortDescription": "string",
                "price": "decimal"
            }
        ],
        "total": "decimal"
    }
    ```

- **Response**:

    ```json
    {
        "id": "string"
    }
    ```

### Get Points

- **URL**: `/receipts/{id}/points`
- **Method**: `GET`
- **Response**:

    ```json
    {
        "points": "integer"
    }
    ```

## Running Tests

1. Open a new terminal:

2. Run the tests inside the same docker container:

    ```bash
    docker exec -it fastserver pytest
    ```
