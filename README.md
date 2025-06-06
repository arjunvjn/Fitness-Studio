# Fitness Studio

## 📋 Description
This is a RESTful API built with Django REST Framework for managing a fitness studio. It provides endpoints for user registration, authentication (login and logout), fitness class creation, viewing available classes, booking class slots, and retrieving details of booked slots.


## 🚀 Features
- User/Instructor:
    - Creation
    - Authentication (using JWT)
    - Logout

- Fitness Studio:
    - Fitness class creation.
    - Showing available fitness class slots.
    - Booking a fitness class slot.
    - Showing details of the booked slot by a particular user.

- Role-based access control (User, Instructor) using permission classes.
- Timezone management.

## 🛠️ Technologies Used
- Django Rest Framework
- SQLite
- Django Rest Framework SimpleJWT for authentication

## 🔧 Setup Instructions

### Prerequisites
- Python 3.13+
- pip (Python package installer)
- venv (for creating a virtual environment)

### Installation

```bash
# Clone the repo
git clone https://github.com/arjunvjn/Fitness-Studio.git
cd Fitness-Studio

# Create an virtual environment
python -m venv venv

# Activate the Virtual Environment
# On macOS/Linux
source venv/bin/activate
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# For installing the required packages
cd fitness_studio
pip install -r requirements.txt

# For running the code
python manage.py runserver
```

## 🗄️ Database Design
![Alt Text](./Fitness%20Studio.png)

## 📬 Postman Collection
Postman Documentation link - https://documenter.getpostman.com/view/20668961/2sB2x2KuVE
