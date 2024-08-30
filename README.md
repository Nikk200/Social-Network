
# Social Network

A social networking application that allows users to connect with each other by sending and accepting friend requests, searching for users, and managing their friend lists through a RESTful API built with Django REST Framework.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and login using first name, last name, email, and password (case insensitive).
- Search for other users by email or name with pagination (up to 10 records per page).
- Send, accept, and reject friend requests.
- List of friends (users who have accepted friend requests).
- List of pending friend requests.
- Rate limiting to prevent users from sending more than 3 friend requests within a minute.

## Technologies Used

- **Django**: The web framework used for building the API.
- **Django REST Framework**: A powerful toolkit for building Web APIs.
- **SQLite**: The database used for data storage.
- **Docker**: For containerization of the application.

## Installation

To get a local copy up and running, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Nikk200/social-network.git
   ```
2. Navigate to the project directory:
   ```bash
   cd social-network
   ```
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv env
   ```
4. Activate the virtual environment:
   - For Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     source env/bin/activate
     ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the server, use the following command:

```bash
python manage.py runserver
```

You can then access the API at `http://127.0.0.1:8000/`.

## API Endpoints

- `POST /sign-up/` - User signup with first name, last name, email, and password.
- `POST /sign-in/` - User login with email and password.
- `POST /sign-out/` - User logout (invalidate the session).
- `GET /search-user/` - Search for users by email or name (pagination up to 10 records).
- `POST /send-friend-request/` - Send a friend request to another user.
- `POST /accept-friend-request/<int:request_id>/` - Accept a friend request by ID.
- `POST /reject-friend-request/` - Reject a friend request.
- `GET /list-friends/` - List all friends (users who have accepted friend requests).
- `GET /list-pending-requests/` - List all pending friend requests received.


### Example Request/Response

#### User Signup
- **Request**:
    ```json
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "yourpassword"
    }
    ```

- **Response**:
    ```json
    {
        "message": "User created successfully."
    }
    ```

#### User Login
- **Request**:
    ```json
    {
        "email": "john.doe@example.com",
        "password": "yourpassword"
    }
    ```

- **Response**:
    ```json
    {
        "message": "Login successful."
    }
    ```

#### Search User
- **Request**:
    ```http
    GET /search-user/?keyword=am
    ```

- **Response**:
    ```json
    [
        {
            "id": 1,
            "first_name": "Amarendra",
            "last_name": "Singh",
            "email": "amar@example.com"
        },
        {
            "id": 2,
            "first_name": "Amar",
            "last_name": "Kumar",
            "email": "amar2@example.com"
        },
        {
            "id": 3,
            "first_name": "Aman",
            "last_name": "Verma",
            "email": "aman@example.com"
        }
    ]
    ```

#### Send Friend Request
- **Request**:
    ```json
    {
        "receiver_id": 2
    }
    ```

- **Response**:
    ```json
    {
        "message": "Friend request sent."
    }
    ```

#### Accept Friend Request
- **Request**:
    ```http
    POST /accept-friend-request/1/
    ```

- **Response**:
    ```json
    {
        "message": "Friend request accepted."
    }
    ```

#### List Friends
- **Request**:
    ```http
    GET /list-friends/
    ```

- **Response**:
    ```json
    [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        },
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com"
        }
    ]
    ```

#### List Pending Requests
- **Request**:
    ```http
    GET /list-pending-requests/
    ```

- **Response**:
    ```json
    [
        {
            "id": 1,
            "sender": {
                "id": 3,
                "first_name": "Alice",
                "last_name": "Johnson",
                "email": "alice@example.com"
            }
        }
    ]
    ```

### Docker Setup

To containerize and run the application using Docker, follow these steps:

1. Ensure Docker is installed and running on your system. For Windows, make sure Docker Desktop is running and that your terminal has elevated privileges (run as administrator).

2. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

   This command will:
   - Build the Docker images as specified in the `Dockerfile`.
   - Start the containers as defined in `docker-compose.yml`.
   - Run the Django application inside a Docker container, accessible at `http://localhost:8000`.

   
### Notes

- Ensure that all endpoints (except signup and login) require authentication.
- Implement rate limiting to restrict users from sending more than 3 friend requests within a minute.

## Testing

To run the tests for your project, use the following command:

```bash
python manage.py test
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create your feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

