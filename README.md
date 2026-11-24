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

### Prerequisites
- Python installed.
- Git installed (optional if downloading the repository as a ZIP).

### Installation

1. Clone this repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Open the project directory:

   ```bash
   cd DataStraw-Roster-System
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python -m streamlit run app.py
   ```

5. Open the local URL displayed in your terminal.

## Live Application

[Open DataStraw Live App](https://datastraw-roster-system-99irkn3beopcuae8k2atne.streamlit.app/)

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

**Project:** DataStraw Smart Roster Management System

**Technology:** Python, Streamlit and SQLite

## Tell Us How You Think

### 1. How did you structure your database, and why?

I used SQLite to store the application data in separate tables for employees, brands, processes, pods, assignments, availability, and monthly rosters. This structure keeps the data organized and makes it easier to manage relationships between employees and processes. I used foreign keys to connect related records.

### 2. How does your roster generation logic work?

The roster is generated month-wise. The system considers active employees, their process assignments, and their availability. Sundays are marked as weekly offs, while employees with leave or other availability records are handled accordingly. Eligible employees are assigned to processes based on staffing requirements, with workload balancing to distribute shifts more evenly. Coverage gaps are identified separately.

### 3. How does your system handle one employee working across multiple brands or processes?

The assignments table allows an employee to be associated with multiple processes. During roster generation, the system checks those assignments and ensures that an employee is not allocated to more than one process on the same day.

### 4. What happens when an employee is unavailable?

Employees marked as on leave, weekly off, or comp-off are excluded from normal work allocation for the affected date. If this causes a process to have fewer employees than required, the system identifies the coverage gap. A manager can then review and make manual changes.

### 5. What conflicts does your system detect?

The system identifies availability-related conflicts, including leave and weekly-off conflicts, as well as process coverage gaps, unassigned employees, and missing roster entries. These checks help managers identify issues that need attention.

### 6. Which parts are automated, and which require human decisions?

Employee and process management, monthly roster generation, basic workload balancing, and coverage checks are automated. Managers can manually edit roster entries and make final decisions when resolving staffing gaps or operational requirements.

### 7. How would you scale this system for a larger organization?

I would move from SQLite to PostgreSQL, introduce role-based access, improve database indexing, and add automated testing. For larger scheduling requirements, I would consider a dedicated optimization engine to handle more complex allocation rules.

### 8. What would you improve next?

I would first add configurable working calendars for each brand and process, including public holidays and different weekly-off rules. Next, I would improve conflict resolution with backup employee recommendations, add authentication, enable roster export, and use persistent cloud database storage.
