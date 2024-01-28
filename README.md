# Phone Book Application

## Overview

This project is a simple Phone Book application developed using Python and PyQt5 for the GUI. The application allows users to add contacts to a database, search for contacts based on criteria, update contact information, and delete contacts.

## Files

### 1. `main.py`

This file contains the main application code. It utilizes PyQt5 for the graphical user interface and connects to a PostgreSQL database using the Peewee ORM. The application has two main tabs: "Add Contact" and "Search Contacts."

- **Add Contact Tab:** Allows users to input information for a new contact and add it to the database.
- **Search Contacts Tab:** Enables users to search for contacts based on first name and last name. Search results are displayed in a table, and users can update or delete contacts directly from the table.

### 2. `database_manager.py`

This file defines a `DatabaseManager` class responsible for handling the connection to the PostgreSQL database. It includes methods for connecting to the database, closing the connection, and creating tables.

### 3. `models.py`

This file defines the `Contact` model using Peewee. It represents the structure of the "contacts" table in the database, including fields such as `id`, `first_name`, `last_name`, `phone_number`, and `address`. The file also initializes the database connection, creates the "contacts" table, and closes the connection.

### 4. `local_settings.py`

This file contains the local settings for the database connection, such as the database name, user, password, host, and port.

## Setup and Execution

1. Make sure you have Python installed on your machine.
2. Install the required libraries using the following command:
   ```bash
   pip install PyQt5 peewee
   ```
3. Execute the application by running the `main.py` file:
   ```bash
   python main.py
   ```

## Database Connection

The application connects to a PostgreSQL database using the details specified in the `local_settings.py` file. Ensure that PostgreSQL is installed on your machine and create a database with the specified name and user credentials.

**Database Connection Details:**

- **Database Name:** #Your DataBase Name
- **User:** # Your User in DataBase
- **Password:** #Your Password of database
- **Host:** #your host name
- **Port:** 5432

**Note:** Adjust these settings according to your PostgreSQL setup.

## Dependencies

- PyQt5
- Peewee

## Acknowledgments

This project uses the PyQt5 library for the graphical user interface and the Peewee ORM for database operations. Special thanks to the PyQt and Peewee communities for providing excellent documentation and resources.

**Disclaimer:** This is a basic overview of the project. You may need to customize the database connection details and dependencies based on your system and requirements.
