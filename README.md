# Online-Books-Library-System



## Description

This is Online Books Library pplication  where library provides subscription plans enabling users to borrow books and magazines according to their plan's borrowing limits

## Table of Contents

- [Installation](#installation)
- [Usage Instructions](#usage-Instructions)
- [Project Structure](#Project-Structure)

## Installation

### Prerequisites

- Python 3.7+
- Django

### Steps

1. Clone the repository:

   ```sh
   https://github.com/himanshu2009/Online-Books-Library-System
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the Django server:
   ```sh
   python manage.py runserver
   ```

5.Apply the database migrations

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Createsuper user for accessing admin panel of django

  ```sh
   python manage.py createsuperuser
   ```
7. Paste url http://127.0.0.1:8000/admin/ in browser aftr running step 4 command


## Usage Instructions

1. Ensure the Django server is running.
2. As there is modification in model part one should run migration commands .


## File Structure and Description

Here is an overview of the project's structure and a brief description of each file and directory:

1. main.py file ->  Entry point of our application

3. settings.py -> Contains all the configuration and settings required for the Django framework to run the application.Also mention the installed apps.

4. models.py -> Defines the database schema for library items, users, and transactions, enforcing borrowing limits and tracking subscriptions.

5.views.py -> Handles the API logic for ordering and returning library items, enforcing user limits based on subscription plans.

6.urls.py -> Maps URLs to appropriate views, enabling functionality for borrowing and returning items.

7.serializers.py -> Processes input data and validates it for order and return operations, ensuring correct data handling for library transactions.

8.project/urls.py -> Manages the routing of additional API endpoints to support future features and scalability of the library system.
