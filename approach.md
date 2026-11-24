# DataStraw – Smart Roster Management System
## Project Approach Note

### 1. Overview
DataStraw is a browser-based employee roster management application developed using Python, Streamlit, and SQLite. It is designed to simplify workforce management and monthly roster planning.

### 2. Technology Used
- **Python:** Application logic and roster generation.
- **Streamlit:** User interface.
- **SQLite:** Database management and storage.

### 3. Application Design
The application is divided into modules for:
- Employee Management
- Brand and Process Management
- Pod Management
- Employee Assignments
- Availability and Leave Management
- Monthly Roster Generation
- Coverage and Conflict Checks

### 4. Roster Generation Approach
The system generates monthly rosters using employee assignments and availability records. It considers weekly offs, leave, and comp-offs while allocating employees to their assigned processes. It also attempts to distribute workloads more evenly.

### 5. Validation and Manual Control
The application identifies staffing coverage gaps and availability-related conflicts. Managers can review the generated roster and make manual changes when required.

### 6. Future Improvements
Future improvements could include configurable brand-specific working calendars, public holiday management, automatic backup employee recommendations, user authentication, roster exports, and persistent cloud database storage.

### 7. Conclusion
The project demonstrates how a centralized application can simplify employee management, resource allocation, and monthly roster planning while keeping managers involved in important scheduling decisions.
