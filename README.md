# JobApplicationTracker

This project is a job application tracker that allows users to manage their job applications, track statuses, and receive notifications using Python for the backend and HTML/CSS/JavaScript for the frontend.

## Structure

- **HTML/CSS/JavaScript**: Handles the frontend interface.
- **Python**: Manages backend processing and database interactions.

## Setup

### HTML/CSS/JavaScript
1. Open the `index.html` file in a web browser to view the frontend interface.

### Python
1. Install Python if it is not already installed.
2. Navigate to the project directory and create a virtual environment:
    ```
    python -m venv venv
    ```
3. Activate the virtual environment:
    - On Windows:
        ```
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```
        source venv/bin/activate
        ```
4. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Set up the environment variables by creating a `.env` file in the root directory with the following content:
    ```
    FLASK_APP=main.py
    DATABASE_URL=sqlite:///applications.db
    ```
6. Initialize the database:
    ```
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```
7. Run the Python application:
    ```
    flask run
    ```

## Overview

1. HTML/CSS/JavaScript provides a user interface for managing job applications, viewing application details, and updating statuses.
2. Python processes the application and user data, interacts with the database, and handles requests.
3. Notifications are sent to users for relevant events such as application status updates and interview reminders.
