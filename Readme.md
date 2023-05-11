# Payment Gateway

This project is a payment gateway implementation, developed as part of a backend challenge. It provides a RESTful API for processing payments using credit or debit cards.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python (version 3.7 or higher): You can download Python from the official website: https://www.python.org/downloads/
- `make` is installed (for running the provided Makefile).
- pip (Python package installer): pip is usually installed by default with Python. You can check if it's available by running `pip --version` in your terminal. If it's not installed, you can install it using the instructions here: https://pip.pypa.io/en/stable/installing/

Additionally, you may need to install SQLite if you're using a different database. You can download SQLite from the official website: https://www.sqlite.org/download.html

Make sure to verify the installation by running `python3 --version`, `pip --version`, and `sqlite3 --version` in your terminal.


## Installation
> **Note:** If in any of the steps python3 doesn't work, try the commands with python

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd payment-gateway
   ```

2. Install dependencies:
    ```bash
    make install
    ```
    OR
    ```bash
    python3 -m venv venv
	source venv/bin/activate
    pip install -r requirements.txt
    ```

3. To run the application:
    ```bash
    make run
    ```
    OR
    ```bash
    uvicorn main:app --reload
    ```
    This will start the FastAPI server and the application will be accessible at http://localhost:8000.

4. To run unit tests:
    ```bash
    make test
    ```
    OR 
    ```bash
    python3 -m unittest Test/test_payment.py
    ```
    This will run the unit tests.

<br>

# API Endpoints
POST ***/process_payment***: Processes a payment request. Expects a JSON payload with payment details. Returns the payment response in JSON format.
Examples
Process a payment
Endpoint: POST /process_payment

Request Body:
```json
{
  "amount": 100.0,
  "currency": "USD",
  "type": "creditcard",
  "card": {
    "number": "4111111111111111",
    "expirationMonth": "12",
    "expirationYear": "2023",
    "cvv": "123"
  }
}
```

Response:
```json
{
  "amount": 100.0,
  "currency": "USD",
  "type": "creditcard",
  "card": {
    "number": "4111111111111111"
  },
  "status": "success",
  "authorization_code": "a1b2c3d4",
  "time": "2023-05-12T10:00:00",
  "http_status_code": 200
}
```
<br>

> **Note:** The API documentation is automatically generated using Swagger UI. You can access the documentation by visiting http://localhost:8000/docs in your browser while the application is running.

<br>

# Project Structure
The project directory structure is as follows:

- `Main.py`: The main entry point of the application.
- `Models/`: Contains the database models.
- `Database/`: Contains the database-related files.
- `Test/`: Contains unit test cases for the application.
- `Validation/`: Contains the validation checks.

<br>

# Dummy Data
## Dummy Credit Card details:
|id|card_number|expiration_month|expiration_year|cvv|balance|
|--|-----------|----------------|---------------|---|-------|
|1|4111111111111111|12|2023|123|600.0|
|2|5555555555554444|10|2024|456|500.0|
|3|378282246310005|6|2023|789|1500.0|
|4|6011111111111117|9|2025|321|2000.0|
|5|3566002020360505|11|2024|654|800.0|


## Dummy Debit Card details:
|id|card_number|expiration_month|expiration_year|cvv|balance|
|--|-----------|----------------|---------------|---|-------|
|1|4000056655665556|12|2023|123|700.0|
|2|5200828282828210|10|2024|456|1500.0|
|3|6762022399992227|6|2023|789|3000.0|
|4|6331101999990016|9|2025|321|1000.0|
|5|5641821111166669|11|2024|654|2500.0|

