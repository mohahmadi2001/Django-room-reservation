
# Django-reservation-rooms

## Introduction

 Django-reservation-rooms is a web application built using Django and the Django REST Framework. This web application is intended for companies that may have multiple meeting rooms, and various teams within the company are interested in scheduling meetings.
## Features

- **User Authentication**: Register, login, and manage your user account.

- **Display of Active Meeting Rooms**:
        The software should display the available meeting rooms within the company and indicate whether they are currently in use or not.

- **Display of Room Availability Status at Different Times of the Day**:
        The software should show the status of rooms throughout the day, allowing users to reserve meeting rooms based on their preferred time slots.

- **Reservation of a Meeting Room for a Specific Time**:
        Users should have the capability to reserve a meeting room for a specific time slot and receive confirmation details.

- **Administrator Access Level**:
        The presence of an administrator access level that can perform tasks such as deleting a reservation.

- **Sending Reminder Emails to Meeting Participants**:
        The software should have the ability to send reminder emails to meeting participants to ensure their attendance.

## Project Structure

```
.
├── users              # User account management
├── core               # Core functionalities
├── meetings           # meeting management
├── reservations       # reservation management
├── teams               # team management
├── app                # Project settings
├── manage.py          # Django management script
└── requirements       # Project dependencies
```

## Requirements

- Python 3.x
- Django 4.2.5
- Django REST Framework 3.14.0
- djangorestframework-simplejwt==5.3.0
- drf-spectacular==0.26.4
- python-dotenv==1.0.0

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/mohahmadi2001/Django-room-reservation.git
    ```

2. Navigate to the project directory:

    ```
    cd Django-room-reservation
    ```

3. Create a virtual environment and activate it:

    ```
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venvScriptsactivate`
    ```

4. Install the required packages:

    ```
    pip install -r requirements/developments.txt
    ```

5. Apply migrations:

    ```
    python manage.py migrate
    ```

6. Run the server:

    ```
    python manage.py runserver
    ```

## Usage

To use the application, navigate to `http://localhost:8000/` in your web browser. You'll find options to manage meetings and reservations.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
