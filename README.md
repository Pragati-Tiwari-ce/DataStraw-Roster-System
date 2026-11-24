# DataStraw – Smart Roster Management System

## Project Overview

DataStraw is a browser-based employee roster management application built using Python, Streamlit, and SQLite.

It helps managers organize employees, manage brands and processes, assign employees to teams, track availability, generate monthly rosters, and identify scheduling conflicts.

## Technologies Used

- **Python:** Application logic and roster generation.
- **Streamlit:** Web-based user interface.
- **SQLite:** Database for storing employee and roster information.

## Features

### 1. Dashboard
- Displays workforce statistics.
- Shows monthly roster summaries.
- Provides an overview of team distribution.

### 2. Employee Management
- Add new employees.
- Update employee details.
- Delete employee records.
- View employee information.

### 3. Brands & Processes
- Create and manage brands.
- Add processes under brands.
- Configure required employee counts.

### 4. Pod Management
- Create pods.
- Rename pods.
- Assign employees to pods.
- Delete pods.

### 5. Assignments
- Assign employees to processes.
- View existing assignments.
- Manage employee-process relationships.

### 6. Availability & Leaves
- Record employee leave.
- Manage weekly offs.
- Record compensatory offs.
- Remove availability records.

### 7. Monthly Roster
- Generate monthly employee rosters.
- Allocate employees to assigned processes.
- Track working days and weekly offs.
- Edit roster entries manually.
- View process coverage.

### 8. Conflict Detection
- Identify leave conflicts.
- Identify weekly-off conflicts.
- Identify compensatory-off conflicts.
- Detect process coverage gaps.
- Identify missing roster entries.

## Database Structure

The application uses SQLite to manage its data.

Main tables include:
- Employees
- Brands
- Processes
- Pods
- Assignments
- Availability
- Roster

## How to Run Locally

1. Clone this repository.
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python -m streamlit run app.py
   ```

4. Open the local URL displayed in your terminal.

## Live Application

[[Open DataStraw Live App](https://datastraw-roster-system-99irkn3beopcuae8k2atne.streamlit.app/)]

## Current Limitations

- The application uses SQLite local storage.
- Persistent cloud database storage is not configured.
- Advanced automatic roster optimization is not implemented.
- Public holiday calendars and shift timing management are not yet integrated.
- User authentication and role-based access control are not implemented.

## Future Improvements

- Integrate a persistent cloud database.
- Add user authentication and role-based permissions.
- Integrate configurable public holiday calendars.
- Improve roster allocation and workload optimization.
- Add downloadable roster reports.

## Author

Developed as a roster management project using Python, Streamlit, and SQLite.
