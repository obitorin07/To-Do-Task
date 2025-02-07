# To-Do-Task-Python

This is a simple daily to-do list app to track your tasks and progress. It automatically logs your task status each day, fills in missing days as "Incomplete", and displays daily statistics.

## Technologies Used
- **Streamlit** – for the interactive web interface
- **MySQL** – as the database backend
- **mysql-connector-python** – to connect Python with MySQL
- **python-dotenv** – to manage environment variables

## Setup

1. **Database Setup:**  
   Run the provided `database.sql` to create the `to_do_task` database and necessary tables.

2. **Environment Variables:**  
   Create a file named `credentials.env` in the project root with the following dummy information(replace with actual information):
   ```env
   host='localhost'
   database='database_name'
   user='username'
   password='password'
