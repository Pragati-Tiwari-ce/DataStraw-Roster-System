
import sqlite3
from datetime import date
# Connect to the database
def get_connection():
    conn = sqlite3.connect("roster.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# Create employee table
def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            pod TEXT NOT NULL,
            designation TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Brands table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active'
        )
    """)

    # Processes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            process_id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_id INTEGER NOT NULL,
            process_name TEXT NOT NULL,
            required_employees INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active',
            FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
            UNIQUE (brand_id, process_name)
        )
    """)
        # Employee Availability and Leaves table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS availability (
            availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            availability_date TEXT NOT NULL,
            availability_type TEXT NOT NULL,
            reason TEXT,

            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
                ON DELETE CASCADE,

            UNIQUE (employee_id, availability_date)
        )
    """)
        # Employee to Process Assignments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            process_id INTEGER NOT NULL,

            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
                ON DELETE CASCADE,

            FOREIGN KEY (process_id)
                REFERENCES processes(process_id)
                ON DELETE CASCADE,

            UNIQUE (employee_id, process_id)
        )
    """)

    # Monthly Roster table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roster (
            roster_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            process_id INTEGER,
            roster_date TEXT NOT NULL,
            status TEXT NOT NULL,

            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
                ON DELETE CASCADE,

            FOREIGN KEY (process_id)
                REFERENCES processes(process_id)
                ON DELETE SET NULL,

            UNIQUE (employee_id, roster_date)
        )
    """)

        # Pods table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pods (
            pod_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pod_name TEXT UNIQUE NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Insert sample employees
def add_sample_employees():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]

    if count == 0:

        sample_employees = [
            ("DS001", "Aarav Sharma", "aarav@datastraw.demo", "Alpha", "Customer Support", "Active"),
            ("DS002", "Priya Patel", "priya@datastraw.demo", "Alpha", "Customer Support", "Active"),
            ("DS003", "Rohan Mehta", "rohan@datastraw.demo", "Alpha", "Team Executive", "Active"),
            ("DS004", "Ananya Singh", "ananya@datastraw.demo", "Alpha", "Customer Support", "Active"),
            ("DS005", "Ishaan Gupta", "ishaan@datastraw.demo", "Alpha", "Team Executive", "Active"),
            ("DS006", "Kavya Nair", "kavya@datastraw.demo", "Alpha", "Customer Support", "Active"),

            ("DS007", "Aditya Verma", "aditya@datastraw.demo", "Beta", "Customer Support", "Active"),
            ("DS008", "Meera Joshi", "meera@datastraw.demo", "Beta", "Team Executive", "Active"),
            ("DS009", "Arjun Rao", "arjun@datastraw.demo", "Beta", "Customer Support", "Active"),
            ("DS010", "Diya Shah", "diya@datastraw.demo", "Beta", "Team Executive", "Active"),
            ("DS011", "Kabir Das", "kabir@datastraw.demo", "Beta", "Customer Support", "Active"),
            ("DS012", "Sana Khan", "sana@datastraw.demo", "Beta", "Team Executive", "Active"),

            ("DS013", "Vivaan Kapoor", "vivaan@datastraw.demo", "Gamma", "Customer Support", "Active"),
            ("DS014", "Ira Malhotra", "ira@datastraw.demo", "Gamma", "Team Executive", "Active"),
            ("DS015", "Reyansh Jain", "reyansh@datastraw.demo", "Gamma", "Customer Support", "Active"),
            ("DS016", "Myra Reddy", "myra@datastraw.demo", "Gamma", "Team Executive", "Active"),
            ("DS017", "Atharv Kulkarni", "atharv@datastraw.demo", "Gamma", "Customer Support", "Active"),
            ("DS018", "Aadhya Iyer", "aadhya@datastraw.demo", "Gamma", "Team Executive", "Active"),

            ("DS019", "Krishna Bose", "krishna@datastraw.demo", "Delta", "Customer Support", "Active"),
            ("DS020", "Sara Thomas", "sara@datastraw.demo", "Delta", "Team Executive", "Active"),
            ("DS021", "Dev Mishra", "dev@datastraw.demo", "Delta", "Customer Support", "Active"),
            ("DS022", "Avni Desai", "avni@datastraw.demo", "Delta", "Team Executive", "Active"),
            ("DS023", "Yash Chawla", "yash@datastraw.demo", "Delta", "Customer Support", "Active"),
            ("DS024", "Riya Sinha", "riya@datastraw.demo", "Delta", "Team Executive", "Active"),

            ("DS025", "Dhruv Bhat", "dhruv@datastraw.demo", "Epsilon", "Customer Support", "Active"),
            ("DS026", "Tara Menon", "tara@datastraw.demo", "Epsilon", "Team Executive", "Active"),
            ("DS027", "Neil Fernandes", "neil@datastraw.demo", "Epsilon", "Customer Support", "Active"),
            ("DS028", "Pihu Agarwal", "pihu@datastraw.demo", "Epsilon", "Team Executive", "Active"),
            ("DS029", "Om Prakash", "om@datastraw.demo", "Epsilon", "Customer Support", "Active"),
            ("DS030", "Kiara Roy", "kiara@datastraw.demo", "Epsilon", "Team Executive", "Active")
        ]

        cursor.executemany("""
            INSERT INTO employees
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_employees)

    conn.commit()
    conn.close()


# Get all employees
def get_employees():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM employees
        ORDER BY employee_id
    """)

    employees = cursor.fetchall()

    conn.close()

    return employees


# Add a new employee
def add_employee(employee_id, name, email, pod, designation):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        employee_id,
        name,
        email,
        pod,
        designation,
        "Active"
    ))

    conn.commit()
    conn.close()


# Update employee details
def update_employee(employee_id, name, email, pod, designation, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET name=?, email=?, pod=?, designation=?, status=?
        WHERE employee_id=?
    """, (
        name,
        email,
        pod,
        designation,
        status,
        employee_id
    ))

    conn.commit()
    conn.close()


# Delete employee
def delete_employee(employee_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM employees
        WHERE employee_id=?
    """, (employee_id,))

    conn.commit()
    conn.close()


# Initialize database
create_database()
add_sample_employees()
def add_brand(brand_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO brands (brand_name) VALUES (?)",
        (brand_name,)
    )

    conn.commit()
    conn.close()


def get_brands():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT brand_id, brand_name, status FROM brands ORDER BY brand_name"
    )

    brands = cursor.fetchall()
    conn.close()
    return brands
def update_brand(brand_id, new_name, new_status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE brands
        SET brand_name = ?, status = ?
        WHERE brand_id = ?
    """, (new_name, new_status, brand_id))

    conn.commit()
    conn.close()


def add_process(brand_id, process_name, required_employees):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO processes
        (brand_id, process_name, required_employees)
        VALUES (?, ?, ?)
    """, (brand_id, process_name, required_employees))

    conn.commit()
    conn.close()


def get_processes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            processes.process_id,
            brands.brand_name,
            processes.process_name,
            processes.required_employees,
            processes.status
        FROM processes
        JOIN brands
        ON processes.brand_id = brands.brand_id
        ORDER BY brands.brand_name, processes.process_name
    """)

    processes = cursor.fetchall()
    conn.close()
    return processes

# Get all employee-process assignments
def get_assignments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            assignments.assignment_id,
            employees.employee_id,
            employees.name,
            processes.process_id,
            brands.brand_name,
            processes.process_name
        FROM assignments
        JOIN employees
            ON assignments.employee_id = employees.employee_id
        JOIN processes
            ON assignments.process_id = processes.process_id
        JOIN brands
            ON processes.brand_id = brands.brand_id
        ORDER BY brands.brand_name, processes.process_name
    """)

    assignments = cursor.fetchall()
    conn.close()
    return assignments


# Assign an employee to a process
def add_assignment(employee_id, process_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assignments (employee_id, process_id)
        VALUES (?, ?)
    """, (employee_id, process_id))

    conn.commit()
    conn.close()


# Remove an employee from a process
def delete_assignment(assignment_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM assignments
        WHERE assignment_id = ?
    """, (assignment_id,))

    conn.commit()
    conn.close()

def update_process(process_id, new_name, required_employees, new_status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE processes
        SET process_name = ?,
            required_employees = ?,
            status = ?
        WHERE process_id = ?
    """, (
        new_name,
        required_employees,
        new_status,
        process_id
    ))

    conn.commit()
    conn.close()
def delete_process(process_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM processes WHERE process_id = ?",
        (process_id,)
    )

    conn.commit()
    conn.close()
def seed_existing_pods():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT pod FROM employees")

    existing_pods = cursor.fetchall()

    for pod in existing_pods:
        cursor.execute(
            "INSERT OR IGNORE INTO pods (pod_name) VALUES (?)",
            (pod[0],)
        )

    conn.commit()
    conn.close()


def get_pods():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            pods.pod_id,
            pods.pod_name,
            COUNT(employees.employee_id)
        FROM pods
        LEFT JOIN employees
        ON pods.pod_name = employees.pod
        GROUP BY pods.pod_id, pods.pod_name
        ORDER BY pods.pod_name
    """)

    pods = cursor.fetchall()
    conn.close()
    return pods


def add_pod(pod_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO pods (pod_name) VALUES (?)",
        (pod_name,)
    )

    conn.commit()
    conn.close()


def assign_employee_to_pod(employee_id, pod_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET pod = ?
        WHERE employee_id = ?
    """, (pod_name, employee_id))

    conn.commit()
    conn.close()

def rename_pod(old_name, new_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET pod = ?
        WHERE pod = ?
    """, (new_name, old_name))

    cursor.execute("""
        UPDATE pods
        SET pod_name = ?
        WHERE pod_name = ?
    """, (new_name, old_name))

    conn.commit()
    conn.close()


# Initialize database and pods
add_sample_employees()
seed_existing_pods()
def delete_pod(pod_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM employees WHERE pod = ?",
        (pod_name,)
    )

    employee_count = cursor.fetchone()[0]

    if employee_count > 0:
        conn.close()
        return False

    cursor.execute(
        "DELETE FROM pods WHERE pod_name = ?",
        (pod_name,)
    )

    conn.commit()
    conn.close()

    return True
# Get all availability records
def get_availability():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            availability.availability_id,
            employees.employee_id,
            employees.name,
            availability.availability_date,
            availability.availability_type,
            availability.reason
        FROM availability
        JOIN employees
        ON availability.employee_id = employees.employee_id
        ORDER BY availability.availability_date
    """)

    records = cursor.fetchall()
    conn.close()
    return records


# Add availability record
def add_availability(employee_id, availability_date, availability_type, reason):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO availability
        (employee_id, availability_date, availability_type, reason)
        VALUES (?, ?, ?, ?)
    """, (employee_id, availability_date, availability_type, reason))

    conn.commit()
    conn.close()


# Delete availability record
def delete_availability(availability_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM availability
        WHERE availability_id = ?
    """, (availability_id,))

    conn.commit()
    conn.close()

# Generate monthly roster
def generate_month_roster(year, month):

    conn = get_connection()
    cursor = conn.cursor()

    employees = get_employees()
    processes = get_processes()
    assignments = get_assignments()
    availability = get_availability()

    active_employees = {
        emp[0]: emp for emp in employees if emp[5] == "Active"
    }

    active_processes = [
        process for process in processes if process[4] == "Active"
    ]

    employee_processes = {}

    for assignment in assignments:
        employee_id = assignment[1]
        process_id = assignment[3]

        if employee_id in active_employees:
            employee_processes.setdefault(process_id, []).append(employee_id)

    availability_map = {
        (record[1], record[3]): record[4]
        for record in availability
    }

    month_key = f"{year}-{month:02d}"

    # Replace existing roster for this month
    cursor.execute(
        "DELETE FROM roster WHERE substr(roster_date, 1, 7) = ?",
        (month_key,)
    )

    import calendar
    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):

        roster_date = f"{year}-{month:02d}-{day:02d}"
        current_date = date(year, month, day)

        daily_status = {}
        used_employees = set()

        # First mark employees who are unavailable
        for employee_id in active_employees:

            availability_type = availability_map.get(
                (employee_id, roster_date)
            )

            if availability_type:
                daily_status[employee_id] = availability_type

            elif current_date.weekday() == 6:
                daily_status[employee_id] = "Weekly Off"

            else:
                daily_status[employee_id] = "Unassigned"

        # Allocate available employees to processes
        for process in active_processes:

            process_id = process[0]
            required = process[3]

            assigned_pool = employee_processes.get(process_id, [])

            if assigned_pool:
                rotation = (day - 1) % len(assigned_pool)
                assigned_pool = (
                    assigned_pool[rotation:] +
                    assigned_pool[:rotation]
                )

            allocated = 0

            for employee_id in assigned_pool:

                if allocated >= required:
                    break

                if employee_id in used_employees:
                    continue

                if daily_status[employee_id] != "Unassigned":
                    continue

                daily_status[employee_id] = "Working"
                used_employees.add(employee_id)
                allocated += 1

                cursor.execute("""
                    INSERT INTO roster
                    (employee_id, process_id, roster_date, status)
                    VALUES (?, ?, ?, ?)
                """, (
                    employee_id,
                    process_id,
                    roster_date,
                    "Working"
                ))

        # Save remaining employees
        for employee_id, status in daily_status.items():

            if status != "Working":
                cursor.execute("""
                    INSERT INTO roster
                    (employee_id, process_id, roster_date, status)
                    VALUES (?, NULL, ?, ?)
                """, (
                    employee_id,
                    roster_date,
                    status
                ))

    conn.commit()
    conn.close()



# Get monthly roster
def get_month_roster(year, month):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            roster.roster_id,
            roster.roster_date,
            employees.employee_id,
            employees.name,
            employees.pod,
            brands.brand_name,
            processes.process_name,
            roster.status
        FROM roster
        JOIN employees
            ON roster.employee_id = employees.employee_id
        LEFT JOIN processes
            ON roster.process_id = processes.process_id
        LEFT JOIN brands
            ON processes.brand_id = brands.brand_id
        WHERE substr(roster.roster_date, 1, 7) = ?
        ORDER BY roster.roster_date, employees.name
    """, (f"{year}-{month:02d}",))

    records = cursor.fetchall()
    conn.close()

    return records


# Manually update a roster entry
def update_roster_entry(roster_id, process_id, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE roster
        SET process_id = ?, status = ?
        WHERE roster_id = ?
    """, (process_id, status, roster_id))

    conn.commit()
    conn.close()
