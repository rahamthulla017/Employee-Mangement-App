# Employee Management App

A comprehensive Employee Management System built with Django. This application allows for managing employees, tasks, projects, and notifications with role-based access control.

## Features

- **User Authentication**: Secure signup and login for Admins, Managers, and Employees.
- **Dashboard**: Role-specific dashboards for employees and admins.
- **Task Management**: Create, assign, and track tasks.
- **Project Management**: Manage projects and associate tasks with them.
- **Notifications**: System for notifying users of important updates.
- **Analytics**: insights into task completion and employee performance.
- **Responsive Design**: Modern UI accessible on various devices.

## Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (default), extensible to PostgreSQL/MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Containerization**: Docker

## Getting Started

### Prerequisites

- Python 3.10+ installed
- Git
- Docker (optional)

### Local Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd "Employee Management app"
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    Access the app at `http://127.0.0.1:8000`.

### Running with Docker

1.  **Build the Docker image:**

    ```bash
    docker build -t employee-management-app .
    ```

2.  **Run the container:**

    ```bash
    docker run -p 8000:8000 employee-management-app
    ```

    Access the app at `http://localhost:8000`.

## Project Structure

- `accounts/`: User authentication and profile management.
- `tasks/`: Task and project management logic.
- `notifications/`: Notification system.
- `analytics/`: Data analysis and reporting.
- `templates/`: HTML templates.
- `config/`: Project main configuration.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
