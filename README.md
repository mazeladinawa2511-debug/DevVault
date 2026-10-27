DevVault

DevVault is a Flask web application for managing projects with user authentication and individual project ownership.

Features

- User registration and login
- Secure password hashing
- Session management
- Create and view projects
- Edit and delete projects
- Project ownership and access control
- Database migrations with Flask-Migrate
- Automated tests with pytest

Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-WTF
- SQLite
- pytest

Setup

Create and activate a virtual environment, then install dependencies:

python -m venv .venv
python -m pip install -r requirements.txt

Create a ".env" file or configure environment variables for deployment. Set a strong "SECRET_KEY" before running in production.

Database

Initialize or update the database schema:

flask --app run db upgrade

Run the Application

python run.py

Run Tests

python -m pytest -v

Security Notes

- Passwords are stored as hashes.
- Project routes require authentication.
- Users can only edit or delete their own projects.
- Use a strong secret key and HTTPS in production.

Status

Early development.
