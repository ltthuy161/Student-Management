# Student Management System

## Overview
This is a simple student management system implemented in Python. It allows users to add, update, delete, and search for students. The data is stored in a JSON file for persistence.

## Project Structure
- `students.json`: Stores student data in JSON format.
- `student_management.py`: The main script containing all functionalities.

## Requirements
- Python 3.x

## Installation
1. Clone this repository or download the source code.
2. Ensure you have Python installed on your system.

## How to Run
1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the program using:
   ```sh
   python student_management.py
   ```

## Features
- **Add Student**: Enter student details and save them to `students.json`.
- **Delete Student**: Remove a student by their ID.
- **Update Student**: Modify existing student information.
- **Search Student**: Find a student by ID or name.
- **Student search by faculty and name**: Find students by their faculty and name.
- **CSV Import/Export**: Import student data from a CSV file and export student data to a CSV file.
- **Rename valid faculty and student status**: Update the names of faculties and student statuses to ensure they are valid and consistent.
- **Logging mechanism**: Track and record system events and errors.
- **Show Version**: Display the current version of the student management system and the build date.

## Data Validation
The program performs validation for:
- **Email format**
- **Phone number format** (10-11 digits)
- **Gender** (1 for Female, 2 for Male)
- **Department** (Must be from predefined list)
- **Student Status** (Must be from predefined list)

## License
This project is open-source and free to use.