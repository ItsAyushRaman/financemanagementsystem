# Finance Tracking System - Backend Assignment

## Overview
This project is a back-end implementation of a Finance Tracking System.. The backend provides an efficient structure for keeping track of incomes, expenses, categories, transaction notes, and financial summaries.

## Technology Stack & Architectural Choices
This project utilizes modern Python development practices. I chose **FastAPI** as the web framework because it inherently implements Pydantic for validation and generates interactive API documentation out of the box (Swagger / Redoc), drastically improving the developer/client experience.

- **FastAPI**: Provides simple, fast, and structured routing. It's fully asynchronous (though we use synchronous DB calls here to align with SQLite limits), and strictly typed.
- **SQLAlchemy (ORM)**: Clean data persistence and relational mapping to our relational database.
- **SQLite**: Used for persistence to eliminate containerization/setup overhead during reviewer assessment. Simply run the project without a Postgres container. The transition to PostgreSQL requires literally changing one line in the settings.
- **Pydantic V2**: Reusable logic for inputs/schemas/serialization, ensuring incoming requests are tightly validated before hitting any database layer. 
- **Pytest**: Used for unit tests, ensuring reliability before scaling up.

## Project Structure (Separation of Concerns)
```text
├── app/
│   ├── api/
│   │   ├── endpoints/       # Route handling for grouped concepts (Auth, Transactions)
│   │   ├── deps.py          # FastAPI dependency injection (e.g. security, DB sessions)
│   ├── core/
│   │   ├── config.py        # Environment variables & constants
│   │   ├── database.py      # SQLAlchemy connection & session creation
│   │   ├── security.py      # JWT implementation & Pwd Hashing
│   ├── models/
│   │   ├── domain.py        # SQLAlchemy entities (User, Transaction)
│   ├── schemas/
│   │   ├── dto.py           # Pydantic models for Data Transfer Objects
│   ├── services/
│   │   ├── transactions.py  # Business logic isolated from API controllers
│   ├── main.py              # Application entrypoint
├── tests/
│   ├── test_api.py          # Unit tests with a separate SQLite test.db
├── requirements.txt         # Dependencies
```

## Features Implemented
1. **User Auth & Role Management**: Endpoint allowing users to register and login as either `Viewer`, `Analyst`, or `Admin`.
   - `Viewer` - Read-only access to transactions / summaries.
   - `Analyst` - Read, Summary access, Create, Update (cannot delete).
   - `Admin` - Full CRUD capabilities on transactions.
2. **Transaction Management System**: Endpoints built for managing user-specific transactions. Supports Create, Read, Update, Delete.
3. **Data Summarization Analytics**: Includes endpoint to fetch Total Income, Total Expenses, Current Balance, and Category-based breakdowns filtered by the current user context.
4. **Input Validation**: Hard bounds on inputs (amounts > 0, strict types `income | expense`).
5. **Secure Authentication**: End-to-end JWT integration + Bcrypt password hashing.

## Setup Instructions

1. **Clone/Download the repository**
2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Access Interactive Docs**
   - Automatically generated docs are available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Here, interact directly with the Swagger UI. Create a user (e.g., set role to `Admin`), copy login payload locally or just use the UI `Authorize` button.
   
6. **Running the Unit Tests**
   ```bash
   pytest -v
   ```

## Quick Usage Guide
 Go to [http://127.0.0.1:8000] local, Deployed - https://financemanagementsystem-rhhp.onrender.com/
- Register a new user (e.g., `admin_user` with role `Admin`).
- Login with the new user to receive a JWT token.
- You can also use Admin, Admin for Quick testing.
- You Must be an Admin to perform all the CRUD operations.


Thank you for viewing.
