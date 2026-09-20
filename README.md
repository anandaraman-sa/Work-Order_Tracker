# FastAPI Work Order Tracker

A simple RESTful API built with **FastAPI** for creating and managing work orders.

The project demonstrates:

* FastAPI REST API development
* Pydantic request/response validation
* CRUD-style API operations
* HTTP status codes
* Structured error handling
* `HTTPException`
* Automatic Swagger/OpenAPI documentation
* UUID-based work-order IDs

> **Note:** This version uses an in-memory dictionary as the data store. Data will be lost when the application restarts.

---

## Features

The API provides four main endpoints:

| Method  | Endpoint                   | Description              |
| ------- | -------------------------- | ------------------------ |
| `POST`  | `/work-orders`             | Create a new work order  |
| `GET`   | `/work-orders`             | Get all work orders      |
| `GET`   | `/work-orders/{id}`        | Get a work order by ID   |
| `PATCH` | `/work-orders/{id}/status` | Update work-order status |

---

## Technology Stack

* **Python 3.10+**
* **FastAPI**
* **Pydantic**
* **Uvicorn**
* REST API
* OpenAPI / Swagger

---

## Project Structure

```text
work-order-api/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/work-order-api.git
```

Navigate to the project:

```bash
cd work-order-api
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

You can test all four endpoints directly from Swagger UI.

---

# API Endpoints

## 1. Create Work Order

### Request

```http
POST /work-orders
```

### Request Body

```json
{
  "title": "Fix network printer",
  "description": "Printer is not connecting to the office network",
  "assigned_to": "John"
}
```

### Response

**HTTP 201 Created**

```json
{
  "id": "7b8f1c7e-5c6c-4a0c-9a12-8e9d8a123456",
  "title": "Fix network printer",
  "description": "Printer is not connecting to the office network",
  "assigned_to": "John",
  "status": "open"
}
```

A new work order is automatically assigned:

```text
status = open
```

---

## 2. List All Work Orders

### Request

```http
GET /work-orders
```

### Response

**HTTP 200 OK**

```json
[
  {
    "id": "7b8f1c7e-5c6c-4a0c-9a12-8e9d8a123456",
    "title": "Fix network printer",
    "description": "Printer is not connecting to the office network",
    "assigned_to": "John",
    "status": "open"
  }
]
```

If there are no work orders:

```json
[]
```

---

## 3. Get Work Order By ID

### Request

```http
GET /work-orders/{work_order_id}
```

Example:

```http
GET /work-orders/7b8f1c7e-5c6c-4a0c-9a12-8e9d8a123456
```

### Response

**HTTP 200 OK**

```json
{
  "id": "7b8f1c7e-5c6c-4a0c-9a12-8e9d8a123456",
  "title": "Fix network printer",
  "description": "Printer is not connecting to the office network",
  "assigned_to": "John",
  "status": "open"
}
```

### Work Order Not Found

If the ID doesn't exist:

**HTTP 404 Not Found**

```json
{
  "detail": {
    "error": "WorkOrderNotFound",
    "message": "Work order '...' was not found"
  }
}
```

---

## 4. Update Work Order Status

### Request

```http
PATCH /work-orders/{work_order_id}/status
```

Example:

```http
PATCH /work-orders/7b8f1c7e-5c6c-4a0c-9a12-8e9d8a123456/status
```

### Request Body

```json
{
  "status": "in_progress"
}
```

### Available Statuses

```text
open
in_progress
completed
cancelled
```

### Response

**HTTP 200 OK**

```json
{
  "id": "7b8f1c7e-5c6c-4a0c-9a12-8e9d8a123456",
  "title": "Fix network printer",
  "description": "Printer is not connecting to the office network",
  "assigned_to": "John",
  "status": "in_progress"
}
```

---

# Validation

The API uses **Pydantic** models to validate incoming requests.

For example, the work-order title must contain at least 3 characters.

```python
class WorkOrderCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5, max_length=500)
    assigned_to: str = Field(..., min_length=2, max_length=100)
```

Invalid input will return an HTTP `422` response.

Example:

```json
{
  "error": "ValidationError",
  "message": "Invalid request data",
  "details": [
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "title"
      ],
      "msg": "String should have at least 3 characters"
    }
  ]
}
```

---

# Error Handling

The application uses FastAPI's `HTTPException` for API errors.

For example, requesting a work order that doesn't exist returns:

```http
404 Not Found
```

with a structured response:

```json
{
  "detail": {
    "error": "WorkOrderNotFound",
    "message": "Work order was not found"
  }
}
```

Request validation errors are handled using a custom exception handler:

```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    ...
```

# License

This project is available for learning and demonstration purposes.

---

## Author

**Your Name**

GitHub: `https://github.com/<your-username>`
