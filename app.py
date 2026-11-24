import sqlite3
import calendar
#import pandas as pd
from database import (
    get_employees,
    get_availability,
    add_availability,
    delete_availability,
    add_employee,
    update_employee,
    delete_employee,
    add_brand,
        generate_month_roster,
    get_month_roster,
    update_roster_entry,
    get_brands,
    update_brand,
    add_process,
    update_process,
    get_processes,
    delete_process,
    get_pods,
    add_pod,
    assign_employee_to_pod,
    rename_pod,
    delete_pod,
    get_assignments,
    add_assignment,
    delete_assignment
)
import streamlit as st
from datetime import date

# ---------------- PAGE CONFIGURATION ----------------

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="DataStraw | Smart Roster",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>

/* Application background */
.stApp {
    background-color: #F8FAF9;
    color: #26352D;
}

/* Main content */
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* ===== PREMIUM SIDEBAR ===== */

[data-testid="stSidebar"] {
    background: #20372D;
    border-right: 1px solid #344A3E;
}

[data-testid="stSidebar"] * {
    color: #F5F1E8;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #B9C7BA !important;
}

[data-testid="stSidebar"] hr {
    border-color: #526458;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 7px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 9px 11px;
    border-radius: 7px;
    transition: background 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #344B3E;
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #45634F;
}
/* Headings */
h1 {
    color: #26352D;
    font-size: 27px !important;
    font-weight: 650;
}

h2, h3 {
    color: #34483C;
    font-weight: 600;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #26734D;
    color: white;
    border: 1px solid #26734D;
    border-radius: 6px;
    font-weight: 500;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #1D5C3D;
    border-color: #1D5C3D;
    color: white;
}

/* Input fields */
.stTextInput input,
.stNumberInput input {
    border-radius: 6px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-size: 14px;
    font-weight: 500;
}

/* Dividers */
hr {
    border-color: #E5EAE6;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #68786E;
    font-size: 13px;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #26352D;
    font-size: 25px;
    font-weight: 650;
}
/* ---------- DASHBOARD METRIC CARDS ---------- */

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E5EAE6;
    border-radius: 12px;
    padding: 20px 22px;
    min-height: 145px;
    box-shadow: 0 2px 8px rgba(30, 55, 40, 0.035);
    transition: all 0.2s ease;
}

.metric-card:hover {
    border-color: #A8BBAA;
    box-shadow: 0 5px 16px rgba(30, 55, 40, 0.07);
    transform: translateY(-2px);
}

.metric-icon {
    font-size: 23px;
    margin-bottom: 12px;
}

.metric-label {
    color: #718077;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}

.metric-value {
    color: #26352D;
    font-size: 30px;
    font-weight: 700;
    margin-top: 5px;
}

.small-muted {
    color: #89958D;
    font-size: 12px;
    margin-top: 5px;
}
/* ---------- BUTTON DESIGN ---------- */

.stButton > button {
    background: #26734D;
    color: #FFFFFF;
    border: 1px solid #26734D;
    border-radius: 7px;
    padding: 8px 18px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #1D5C3D;
    color: #FFFFFF;
    border-color: #1D5C3D;
}

.stButton > button:focus {
    box-shadow: 0 0 0 2px #C5D9CA;
    outline: none;
}
/* Darker borders for Streamlit bordered containers */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border: 1.5px solid #84978A !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 5px rgba(32, 55, 45, 0.06) !important;
}
/* Pod Directory cards only */
[class*="st-key-pod_card_"] {
    border: 2px solid #718579 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 6px rgba(32, 55, 45, 0.08);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------


# ---------------- TEMPORARY DATA ----------------

# ---------------- DASHBOARD DATA ----------------

employees = get_employees()
brands = get_brands()
pods = get_pods()

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## ✳ DATASTRAW")
    st.caption("SMART ROSTER SYSTEM")

    st.divider()
    st.caption("WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Employees",
            "Brands & Processes",
            "Pods",
            "Assignments",
            "Availability & Leaves",
            "Monthly Roster",
            "Conflict Detection"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("WORKSPACE STATUS")
    st.markdown("🟢 System Online")
    st.caption("Smart Roster · v1.0")


# ---------------- REUSABLE METRIC CARD ----------------

def metric_card(icon, label, value, description):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="small-muted">{description}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------


if page == "Dashboard":

    from datetime import date

    # ---------------- DASHBOARD DATA ----------------
    employees = get_employees()
    brands = get_brands()
    pods = get_pods()

    total_employees = len(employees)
    active_employees = sum(
        1 for emp in employees if emp[5] == "Active"
    )
    inactive_employees = total_employees - active_employees

    total_brands = len(brands)
    total_pods = len(pods)

    # Current month's roster
    today = date.today()
    month_name = today.strftime("%B %Y")

    roster = get_month_roster(today.year, today.month)

    working_shifts = sum(1 for r in roster if r[7] == "Working")
    weekly_offs = sum(1 for r in roster if r[7] == "Weekly Off")
    leaves = sum(1 for r in roster if r[7] == "Leave")
    comp_offs = sum(1 for r in roster if r[7] == "Comp-Off")
    unassigned = sum(1 for r in roster if r[7] == "Unassigned")

    
    # ---------------- HEADER ----------------
    st.markdown(
        """
        <div style="background-color:#20372D; padding:30px 32px; border-radius:14px; margin-bottom:26px;">
            <div style="color:#B9C7BA; font-size:11px; letter-spacing:2px; font-weight:600;">
                DATASTRAW / OPERATIONS
            </div>
            <div style="color:#FFFFFF; font-size:30px; font-weight:650; margin-top:10px;">
                Workforce Overview
            </div>
            <div style="color:#D0DAD1; font-size:14px; margin-top:8px;">
                Your workforce, teams and monthly roster at a glance.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ---------------- WORKSPACE METRICS ----------------
    st.markdown("### Workforce Summary")
    st.caption("Current employee and operational records.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card(
            "👥", "Total Employees",
            total_employees, "Registered employees"
        )

    with col2:
        metric_card(
            "✓", "Active Employees",
            active_employees, "Available workforce records"
        )

    with col3:
        metric_card(
            "▦", "Total Brands",
            total_brands, "Registered brands"
        )

    with col4:
        metric_card(
            "◈", "Total Pods",
            total_pods, "Organized teams"
        )

    st.write("")

    # ---------------- MONTHLY ROSTER ----------------
    st.markdown("### Monthly Roster")
    st.caption(f"Roster status for {month_name}")

    if roster:

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Working Shifts", working_shifts)

        with col2:
            st.metric("Weekly Offs", weekly_offs)

        with col3:
            st.metric("Leaves", leaves)

        with col4:
            st.metric("Comp-Offs", comp_offs)

        with col5:
            st.metric("Unassigned", unassigned)

    else:
        with st.container(border=True):
            st.markdown("**No monthly roster generated**")
            st.caption(
                "Generate the current month's roster from the Monthly Roster section "
                "to see scheduling statistics here."
            )

    st.divider()

    # ---------------- TEAM DISTRIBUTION ----------------
    st.markdown("### Team Distribution")
    st.caption("Employee distribution across operational pods.")

    if pods:

        pod_columns = st.columns(3)

        for index, pod in enumerate(pods):
            pod_name = pod[1]
            employee_count = pod[2]

            percentage = (
                employee_count / total_employees
                if total_employees > 0 else 0
            )

            with pod_columns[index % 3]:
                with st.container(border=True):
                    st.markdown(f"**{pod_name}**")
                    st.metric("Employees", employee_count)
                    st.progress(percentage)
                    st.caption(f"{percentage:.0%} of total workforce")

    else:
        st.info("No pods have been created yet.")

    st.divider()

    # ---------------- WORKSPACE GUIDE ----------------
    st.markdown("### Workspace")
    st.caption("Manage the different parts of your roster system.")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("**People & Teams**")
            st.caption(
                "Manage employee records, organize pods and "
                "maintain workforce information."
            )

        with st.container(border=True):
            st.markdown("**Brands & Processes**")
            st.caption(
                "Create brands, configure processes and define "
                "their staffing requirements."
            )

    with col2:
        with st.container(border=True):
            st.markdown("**Assignments & Availability**")
            st.caption(
                "Connect employees to processes and record "
                "leaves, weekly offs and comp-offs."
            )

        with st.container(border=True):
            st.markdown("**Roster & Conflict Detection**")
            st.caption(
                "Generate monthly schedules, review coverage "
                "and identify scheduling conflicts."
            )

    st.divider()

    st.caption(
        "DATASTRAW  ·  SMART ROSTER SYSTEM  ·  VERSION 1.0"
    )


elif page == "Employees":

    st.title("👥 Employee Management")
    st.caption("Manage your workforce from one place.")

    employees = get_employees()

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    active_count = sum(1 for emp in employees if emp[5] == "Active")
    inactive_count = len(employees) - active_count

    col1.metric("Total Employees", len(employees))
    col2.metric("Active Employees", active_count)
    col3.metric("Inactive Employees", inactive_count)

    st.divider()

    # Employee tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Directory",
        "➕ Add Employee",
        "✏️ Edit Employee",
        "🗑️ Delete Employee"
    ])

    # DIRECTORY
    with tab1:

        st.subheader("Employee Directory")

        if employees:

            header = st.columns([1, 1.5, 2, 1, 1.5, 1])

            headings = [
                "Employee ID", "Name", "Email",
                "Pod", "Designation", "Status"
            ]

            for col, heading in zip(header, headings):
                col.markdown(f"**{heading}**")

            st.divider()

            for emp in employees:

                row = st.columns([1, 1.5, 2, 1, 1.5, 1])

                for col, value in zip(row, emp):
                    col.write(value)

                st.divider()

        else:
            st.info("No employees found.")

    # ADD EMPLOYEE
    with tab2:

        st.subheader("Add New Employee")

        pod_list = [pod[1] for pod in get_pods()]

        if pod_list:

            with st.form("add_employee_form"):

                col1, col2 = st.columns(2)

                with col1:
                    new_id = st.text_input(
                        "Employee ID",
                        placeholder="Example: DS031"
                    )
                    new_name = st.text_input("Full Name")
                    new_email = st.text_input("Email")

                with col2:
                    new_pod = st.selectbox("Pod", pod_list)

                    new_designation = st.selectbox(
                        "Designation",
                        ["Customer Support", "Team Executive", "Team Lead"]
                    )

                add_button = st.form_submit_button(
                    "Add Employee",
                    use_container_width=True
                )

                if add_button:

                    if not new_id.strip() or not new_name.strip() or not new_email.strip():
                        st.error("Please fill in Employee ID, Name and Email.")

                    else:
                        try:
                            add_employee(
                                new_id.strip(),
                                new_name.strip(),
                                new_email.strip(),
                                new_pod,
                                new_designation
                            )

                            st.success("Employee added successfully!")
                            st.rerun()

                        except sqlite3.IntegrityError:
                            st.error("Employee ID or email already exists.")

        else:
            st.warning("Please create a Pod before adding employees.")

    # EDIT EMPLOYEE
    with tab3:

        st.subheader("Edit Employee Details")

        if employees:

            employee_ids = [emp[0] for emp in employees]

            selected_id = st.selectbox(
                "Select Employee",
                employee_ids,
                key="edit_employee"
            )

            selected_employee = next(
                emp for emp in employees if emp[0] == selected_id
            )

            pod_list = [pod[1] for pod in get_pods()]

            if pod_list:

                with st.form("edit_employee_form"):

                    col1, col2 = st.columns(2)

                    with col1:
                        edit_name = st.text_input(
                            "Name",
                            value=selected_employee[1]
                        )

                        edit_email = st.text_input(
                            "Email",
                            value=selected_employee[2]
                        )

                    with col2:

                        edit_pod = st.selectbox(
                            "Pod",
                            pod_list,
                            index=(
                                pod_list.index(selected_employee[3])
                                if selected_employee[3] in pod_list
                                else 0
                            )
                        )

                        designations = [
                            "Customer Support",
                            "Team Executive",
                            "Team Lead"
                        ]

                        edit_designation = st.selectbox(
                            "Designation",
                            designations,
                            index=(
                                designations.index(selected_employee[4])
                                if selected_employee[4] in designations
                                else 0
                            )
                        )

                        edit_status = st.selectbox(
                            "Status",
                            ["Active", "Inactive"],
                            index=0 if selected_employee[5] == "Active" else 1
                        )

                    update_button = st.form_submit_button(
                        "Save Changes",
                        use_container_width=True
                    )

                    if update_button:

                        if not edit_name.strip() or not edit_email.strip():
                            st.error("Name and email cannot be empty.")

                        else:
                            try:
                                update_employee(
                                    selected_id,
                                    edit_name.strip(),
                                    edit_email.strip(),
                                    edit_pod,
                                    edit_designation,
                                    edit_status
                                )

                                st.success("Employee updated successfully!")
                                st.rerun()

                            except sqlite3.IntegrityError:
                                st.error("That email address is already used.")

            else:
                st.warning("Please create a Pod before editing employees.")

        else:
            st.info("No employees available to edit.")

    # DELETE EMPLOYEE
    with tab4:

        st.subheader("Delete Employee")

        if employees:

            delete_id = st.selectbox(
                "Select Employee ID to delete",
                [emp[0] for emp in employees],
                key="delete_employee"
            )

            st.warning("Deleting an employee is permanent.")

            if st.button("Delete Selected Employee", type="secondary"):

                delete_employee(delete_id)

                st.success(f"Employee {delete_id} deleted.")
                st.rerun()

        else:
            st.info("No employees available to delete.")


elif page == "Brands & Processes":

    st.title("Brand & Process Management")
    st.caption("Manage your business structure and operational processes.")

    brands = get_brands()
    processes = get_processes()

    # Summary metrics
    col1, col2 = st.columns(2)

    col1.metric("Total Brands", len(brands))
    col2.metric("Total Processes", len(processes))

    st.divider()

    # Main navigation
    brand_tab, process_tab = st.tabs([
        "🏢 Brands",
        "⚙️ Processes"
    ])

    # ==================================================
    # BRAND MANAGEMENT
    # ==================================================

    with brand_tab:

        brand_list, add_brand_tab, edit_brand_tab = st.tabs([
            "Brand Directory",
            "Add Brand",
            "Edit Brand"
        ])

        # BRAND DIRECTORY
        with brand_list:

            st.subheader("Brand Directory")

            if brands:

                header = st.columns([1, 3, 2])

                for col, heading in zip(
                    header,
                    ["Brand ID", "Brand Name", "Status"]
                ):
                    col.markdown(f"**{heading}**")

                for brand in brands:

                    row = st.columns([1, 3, 2])

                    for col, value in zip(row, brand):
                        col.write(value)

                    st.divider()

            else:
                st.info("No brands added yet.")

        # ADD BRAND
        with add_brand_tab:

            st.subheader("Add New Brand")

            with st.form("add_brand_form"):

                brand_name = st.text_input(
                    "Brand Name",
                    placeholder="Example: Brand A"
                )

                add_brand_button = st.form_submit_button(
                    "Add Brand",
                    use_container_width=True
                )

                if add_brand_button:

                    if not brand_name.strip():
                        st.error("Please enter a brand name.")

                    else:
                        try:
                            add_brand(brand_name.strip())
                            st.success("Brand added successfully!")
                            st.rerun()

                        except sqlite3.IntegrityError:
                            st.error("This brand already exists.")

        # EDIT BRAND
        with edit_brand_tab:

            st.subheader("Edit Brand Details")

            if brands:

                brand_options = {
                    f"{brand[1]} (ID: {brand[0]})": brand[0]
                    for brand in brands
                }

                selected_brand = st.selectbox(
                    "Select Brand",
                    list(brand_options.keys()),
                    key="edit_brand_select"
                )

                selected_brand_id = brand_options[selected_brand]

                current_brand = next(
                    brand for brand in brands
                    if brand[0] == selected_brand_id
                )

                with st.form("edit_brand_form"):

                    edit_brand_name = st.text_input(
                        "Brand Name",
                        value=current_brand[1]
                    )

                    edit_brand_status = st.selectbox(
                        "Status",
                        ["Active", "Inactive"],
                        index=(
                            0 if current_brand[2] == "Active" else 1
                        )
                    )

                    update_button = st.form_submit_button(
                        "Save Changes",
                        use_container_width=True
                    )

                    if update_button:

                        if not edit_brand_name.strip():
                            st.error("Brand name cannot be empty.")

                        else:
                            try:
                                update_brand(
                                    selected_brand_id,
                                    edit_brand_name.strip(),
                                    edit_brand_status
                                )

                                st.success("Brand updated successfully!")
                                st.rerun()

                            except sqlite3.IntegrityError:
                                st.error(
                                    "A brand with this name already exists."
                                )

            else:
                st.info("Add a brand first before editing.")

    # ==================================================
    # PROCESS MANAGEMENT
    # ==================================================

    with process_tab:

        process_list, add_process_tab, edit_process_tab, delete_process_tab = st.tabs([
            "Process Directory",
            "Add Process",
            "Edit Process",
            "Delete Process"
        ])

        # PROCESS DIRECTORY
        with process_list:

            st.subheader("Process Directory")

            if processes:

                header = st.columns([1.5, 2, 2, 1.5, 1])

                headings = [
                    "Process ID",
                    "Brand",
                    "Process Name",
                    "Required Employees",
                    "Status"
                ]

                for col, heading in zip(header, headings):
                    col.markdown(f"**{heading}**")

                for process in processes:

                    row = st.columns([1.5, 2, 2, 1.5, 1])

                    for col, value in zip(row, process):
                        col.write(value)

                    st.divider()

            else:
                st.info("No processes added yet.")

        # ADD PROCESS
        with add_process_tab:

            st.subheader("Add Process to Brand")

            if brands:

                brand_options = {
                    f"{brand[1]} (ID: {brand[0]})": brand[0]
                    for brand in brands
                }

                with st.form("add_process_form"):

                    selected_process_brand = st.selectbox(
                        "Select Brand",
                        list(brand_options.keys())
                    )

                    process_name = st.text_input(
                        "Process Name",
                        placeholder="Example: Customer Support"
                    )

                    required_employees = st.number_input(
                        "Required Employees",
                        min_value=1,
                        max_value=30,
                        value=2,
                        step=1
                    )

                    add_process_button = st.form_submit_button(
                        "Add Process",
                        use_container_width=True
                    )

                    if add_process_button:

                        if not process_name.strip():
                            st.error("Please enter a process name.")

                        else:
                            try:
                                add_process(
                                    brand_options[selected_process_brand],
                                    process_name.strip(),
                                    int(required_employees)
                                )

                                st.success("Process added successfully!")
                                st.rerun()

                            except sqlite3.IntegrityError:
                                st.error(
                                    "This process already exists under this brand."
                                )

            else:
                st.info("Add a brand before creating processes.")

        # EDIT PROCESS
        with edit_process_tab:

            st.subheader("Edit Process Details")

            if processes:

                process_options = {
                    f"{process[2]} - {process[1]} (ID: {process[0]})": process[0]
                    for process in processes
                }

                selected_process = st.selectbox(
                    "Select Process",
                    list(process_options.keys()),
                    key="edit_process_select"
                )

                selected_process_id = process_options[selected_process]

                current_process = next(
                    process for process in processes
                    if process[0] == selected_process_id
                )

                with st.form("edit_process_form"):

                    edit_process_name = st.text_input(
                        "Process Name",
                        value=current_process[2]
                    )

                    edit_required_employees = st.number_input(
                        "Required Employees",
                        min_value=1,
                        max_value=30,
                        value=int(current_process[3]),
                        step=1
                    )

                    edit_process_status = st.selectbox(
                        "Status",
                        ["Active", "Inactive"],
                        index=(
                            0 if current_process[4] == "Active" else 1
                        )
                    )

                    update_process_button = st.form_submit_button(
                        "Save Changes",
                        use_container_width=True
                    )

                    if update_process_button:

                        if not edit_process_name.strip():
                            st.error("Process name cannot be empty.")

                        else:
                            try:
                                update_process(
                                    selected_process_id,
                                    edit_process_name.strip(),
                                    int(edit_required_employees),
                                    edit_process_status
                                )

                                st.success("Process updated successfully!")
                                st.rerun()

                            except sqlite3.IntegrityError:
                                st.error(
                                    "This process already exists under this brand."
                                )

            else:
                st.info("No processes available to edit.")

        # DELETE PROCESS
        with delete_process_tab:

            st.subheader("Delete Process")

            if processes:

                delete_process_options = {
                    f"{process[2]} - {process[1]} (ID: {process[0]})": process[0]
                    for process in processes
                }

                selected_delete_process = st.selectbox(
                    "Select Process to Delete",
                    list(delete_process_options.keys()),
                    key="delete_process_select"
                )

                if st.button(
                    "Delete Selected Process",
                    type="secondary"
                ):
                    st.session_state.confirm_delete_process = True

                if st.session_state.get(
                    "confirm_delete_process", False
                ):

                    st.warning(
                        f"Are you sure you want to delete {selected_delete_process}?"
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Yes, Delete"):

                            delete_process(
                                delete_process_options[selected_delete_process]
                            )

                            st.session_state.confirm_delete_process = False
                            st.success("Process deleted successfully!")
                            st.rerun()

                    with col2:
                        if st.button("Cancel"):

                            st.session_state.confirm_delete_process = False
                            st.rerun()

            else:
                st.info("No processes available to delete.")


elif page == "Pods":

    employees = get_employees()
    pods = get_pods()
    pod_names = [pod[1] for pod in pods]

    total_employees = len(employees)
    total_pods = len(pods)
    active_employees = sum(
        1 for emp in employees if emp[5] == "Active"
    )
    assigned_employees = sum(
        1 for emp in employees if emp[3] in pod_names
    )

    # ---------------- PAGE HEADER ----------------
    st.title("Pods & Teams")
    st.caption(
        "Organize your workforce, monitor team strength "
        "and manage employee allocation."
    )

    st.divider()

    # ---------------- SUMMARY ----------------
    st.markdown("### Workforce Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Pods", total_pods)

    with col2:
        st.metric("Total Employees", total_employees)

    with col3:
        st.metric("Active Employees", active_employees)

    with col4:
        st.metric("Assigned Employees", assigned_employees)

    st.divider()

    # ---------------- POD DIRECTORY ----------------
    st.markdown("### Pod Directory")
    st.caption("View team size and employee details by pod.")

    if pod_names:

        for i in range(0, len(pod_names), 2):

            col1, col2 = st.columns(2)
            current_columns = [col1, col2]

            for j in range(2):

                index = i + j

                if index >= len(pod_names):
                    break

                pod_name = pod_names[index]

                pod_employees = [
                    emp for emp in employees
                    if emp[3] == pod_name
                ]

                active_count = sum(
                    1 for emp in pod_employees
                    if emp[5] == "Active"
                )

                inactive_count = len(pod_employees) - active_count

                with current_columns[j]:

                    with st.container(border=True, key=f"pod_card_{index}"):

                        st.markdown(f"#### {pod_name}")

                        st.caption(
                            f"{len(pod_employees)} team members"
                        )

                        m1, m2 = st.columns(2)

                        m1.metric(
                            "Active",
                            active_count
                        )

                        m2.metric(
                            "Inactive",
                            inactive_count
                        )

                        if pod_employees:

                            with st.expander(
                                "View team members"
                            ):

                                for emp in pod_employees:

                                    status_icon = (
                                        "🟢"
                                        if emp[5] == "Active"
                                        else "⚪"
                                    )

                                    st.markdown(
                                        f"{status_icon} **{emp[1]}**"
                                    )

                                    st.caption(
                                        f"{emp[0]} · {emp[4]}"
                                    )

                        else:
                            st.caption("No employees assigned yet.")

    else:
        st.info("No pods created yet. Create your first pod below.")

    st.divider()

    # ---------------- POD MANAGEMENT ----------------
    st.markdown("### Manage Pods")
    st.caption(
        "Create teams, move employees and maintain pod records."
    )

    tab1, tab2, tab3 = st.tabs(
        ["Create / Rename", "Assign Employee", "Delete Pod"]
    )

    # ---------------- CREATE AND RENAME ----------------
    with tab1:

        create_col, rename_col = st.columns(2)

        with create_col:

            with st.container(border=True):

                st.markdown("#### Create New Pod")
                st.caption("Add a new team to your workspace.")

                with st.form("create_pod_form"):

                    new_pod = st.text_input(
                        "Pod Name",
                        placeholder="e.g. Zeta Operations"
                    )

                    create_button = st.form_submit_button(
                        "Create Pod",
                        use_container_width=True
                    )

                    if create_button:

                        if not new_pod.strip():
                            st.warning("Enter a pod name.")

                        else:
                            try:
                                add_pod(new_pod.strip())
                                st.success("Pod created successfully!")
                                st.rerun()

                            except sqlite3.IntegrityError:
                                st.error("This pod already exists.")

        with rename_col:

            with st.container(border=True):

                st.markdown("#### Rename Pod")
                st.caption("Update an existing team's name.")

                if pod_names:

                    with st.form("rename_pod_form"):

                        selected_pod = st.selectbox(
                            "Select Existing Pod",
                            pod_names
                        )

                        new_pod_name = st.text_input(
                            "New Pod Name"
                        )

                        rename_button = st.form_submit_button(
                            "Save New Name",
                            use_container_width=True
                        )

                        if rename_button:

                            if not new_pod_name.strip():
                                st.warning("Enter a new pod name.")

                            elif new_pod_name.strip() == selected_pod:
                                st.warning(
                                    "The new name is the same as the current name."
                                )

                            else:
                                try:
                                    rename_pod(
                                        selected_pod,
                                        new_pod_name.strip()
                                    )

                                    st.success("Pod renamed successfully!")
                                    st.rerun()

                                except sqlite3.IntegrityError:
                                    st.error(
                                        "A pod with this name already exists."
                                    )

                else:
                    st.info("Create a pod before renaming.")

    # ---------------- ASSIGN EMPLOYEE ----------------
    with tab2:

        with st.container(border=True):

            st.markdown("#### Employee Allocation")
            st.caption(
                "Assign an employee to a pod. "
                "Their existing pod assignment will be updated."
            )

            if employees and pod_names:

                employee_options = {
                    f"{emp[0]} — {emp[1]}": emp[0]
                    for emp in employees
                }

                with st.form("assign_employee_form"):

                    selected_employee = st.selectbox(
                        "Select Employee",
                        list(employee_options.keys())
                    )

                    selected_pod = st.selectbox(
                        "Assign To Pod",
                        pod_names
                    )

                    assign_button = st.form_submit_button(
                        "Update Assignment",
                        use_container_width=True
                    )

                    if assign_button:

                        employee_id = employee_options[
                            selected_employee
                        ]

                        assign_employee_to_pod(
                            employee_id,
                            selected_pod
                        )

                        st.success(
                            "Employee assignment updated successfully!"
                        )
                        st.rerun()

            else:
                st.info(
                    "You need at least one employee and one pod "
                    "before assigning employees."
                )

    # ---------------- DELETE POD ----------------
    with tab3:

        with st.container(border=True):

            st.markdown("#### Remove a Pod")
            st.caption(
                "Only empty pods can be deleted. "
                "Reassign their employees before deletion."
            )

            if pod_names:

                with st.form("delete_pod_form"):

                    selected_delete_pod = st.selectbox(
                        "Select Pod",
                        pod_names
                    )

                    delete_button = st.form_submit_button(
                        "Delete Selected Pod",
                        use_container_width=True
                    )

                    if delete_button:

                        result = delete_pod(selected_delete_pod)

                        if result:
                            st.success("Pod deleted successfully!")
                            st.rerun()

                        else:
                            st.error(
                                "This pod still has employees assigned. "
                                "Reassign them before deleting."
                            )

            else:
                st.info("There are no pods to delete.")


elif page == "Assignments":

    employees = get_employees()
    processes = get_processes()
    assignments = get_assignments()

    active_employees = [
        emp for emp in employees if emp[5] == "Active"
    ]

    # ---------------- HEADER ----------------
    st.title("Resource Assignments")
    st.caption(
        "Allocate employees to brand processes and monitor resource coverage."
    )

    st.divider()

    # ---------------- SUMMARY ----------------
    total_processes = len(processes)
    total_assignments = len(assignments)
    total_required = sum(p[3] for p in processes)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Processes", total_processes)
    col2.metric("Active Employees", len(active_employees))
    col3.metric("Current Assignments", total_assignments)
    col4.metric("Required Resources", total_required)

    st.divider()

    # ---------------- TABS ----------------
    tab1, tab2, tab3 = st.tabs(
        ["Process Overview", "New Assignment", "Manage Assignments"]
    )

    # ---------------- PROCESS OVERVIEW ----------------
    with tab1:

        st.markdown("### Process Allocation")
        st.caption("Compare required resources with current assignments.")

        if processes:

            for process in processes:

                process_id = process[0]
                brand_name = process[1]
                process_name = process[2]
                required = process[3]
                status = process[4]

                process_assignments = [
                    a for a in assignments if a[3] == process_id
                ]

                assigned_count = len(process_assignments)
                remaining = max(required - assigned_count, 0)

                with st.container(border=True):

                    st.markdown(f"#### {process_name}")
                    st.caption(f"{brand_name}  ·  {status}")

                    c1, c2, c3 = st.columns(3)

                    c1.metric("Required", required)
                    c2.metric("Assigned", assigned_count)
                    c3.metric("Remaining", remaining)

                    progress = min(
                        assigned_count / max(required, 1),
                        1.0
                    )

                    st.progress(progress)

                    if assigned_count >= required:
                        st.success("Required coverage achieved.")
                    else:
                        st.warning(
                            f"{remaining} more employee(s) needed."
                        )

                    if process_assignments:

                        st.markdown("**Assigned Employees**")

                        for assignment in process_assignments:
                            st.write(
                                f"• {assignment[2]} "
                                f"({assignment[1]})"
                            )

                    else:
                        st.caption("No employees assigned yet.")

        else:
            st.info(
                "No processes available. Add processes under Brands & Processes first."
            )

    # ---------------- NEW ASSIGNMENT ----------------
    with tab2:

        st.markdown("### Assign Employee")
        st.caption("Select a process and allocate an active employee.")

        active_processes = [
            p for p in processes if p[4] == "Active"
        ]

        if active_processes and active_employees:

            process_options = {
                f"{p[1]} — {p[2]}": p[0]
                for p in active_processes
            }

            selected_process_label = st.selectbox(
                "Select Brand / Process",
                list(process_options.keys()),
                key="new_assignment_process"
            )

            selected_process_id = process_options[
                selected_process_label
            ]

            already_assigned = [
                a[1] for a in assignments
                if a[3] == selected_process_id
            ]

            available_employees = [
                emp for emp in active_employees
                if emp[0] not in already_assigned
            ]

            st.caption(
                f"Currently assigned: {len(already_assigned)}"
            )

            if available_employees:

                employee_options = {
                    f"{emp[0]} — {emp[1]} ({emp[3]})": emp[0]
                    for emp in available_employees
                }

                selected_employee_label = st.selectbox(
                    "Select Employee",
                    list(employee_options.keys()),
                    key="new_assignment_employee"
                )

                if st.button(
                    "Assign Employee",
                    key="add_process_assignment",
                    use_container_width=True
                ):

                    employee_id = employee_options[
                        selected_employee_label
                    ]

                    try:
                        add_assignment(
                            employee_id,
                            selected_process_id
                        )

                        st.success("Employee assigned successfully!")
                        st.rerun()

                    except sqlite3.IntegrityError:
                        st.error(
                            "This employee is already assigned to this process."
                        )

            else:
                st.warning(
                    "All active employees are already assigned to this process."
                )

        elif not active_processes:
            st.info("No active processes available.")

        else:
            st.info("No active employees available.")

    # ---------------- MANAGE ASSIGNMENTS ----------------
    with tab3:

        st.markdown("### Current Assignments")
        st.caption("Review and remove existing employee allocations.")

        if assignments:

            for assignment in assignments:

                st.write(
                    f"**{assignment[2]}**  ·  "
                    f"{assignment[4]} / {assignment[5]}"
                )

                st.caption(
                    f"Employee ID: {assignment[1]}  "
                    f"· Assignment ID: {assignment[0]}"
                )

                st.divider()

            assignment_options = {
                (
                    f"{a[2]} — {a[4]} / {a[5]} "
                    f"({a[1]})"
                ): a[0]
                for a in assignments
            }

            selected_assignment = st.selectbox(
                "Select Assignment to Remove",
                list(assignment_options.keys()),
                key="remove_assignment_select"
            )

            if st.button(
                "Remove Assignment",
                key="remove_process_assignment",
                use_container_width=True
            ):

                delete_assignment(
                    assignment_options[selected_assignment]
                )

                st.success("Assignment removed successfully!")
                st.rerun()

        else:
            st.info("No employee assignments have been created yet.")

elif page == "Availability & Leaves":

    st.title("Availability & Leaves")
    st.caption("Manage employee leaves, weekly offs and compensatory offs.")

    employees = get_employees()
    active_employees = [
        emp for emp in employees if emp[5] == "Active"
    ]

    records = get_availability()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Active Employees", len(active_employees))

    with col2:
        st.metric("Total Records", len(records))

    with col3:
        st.metric(
            "Leave Records",
            sum(1 for record in records if record[4] == "Leave")
        )

    st.divider()

    tab1, tab2 = st.tabs(["Add Availability", "Manage Records"])

    with tab1:
        st.subheader("Add Employee Availability")

        if active_employees:

            employee_options = {
                f"{emp[1]} ({emp[0]})": emp[0]
                for emp in active_employees
            }

            with st.form("availability_form"):

                selected_employee = st.selectbox(
                    "Select Employee",
                    list(employee_options.keys())
                )

                selected_date = st.date_input(
                    "Select Date"
                )

                availability_type = st.selectbox(
                    "Availability Type",
                    ["Leave", "Weekly Off", "Comp-Off"]
                )

                reason = st.text_input(
                    "Reason",
                    placeholder="Enter reason (optional)"
                )

                submitted = st.form_submit_button(
                    "Save Record",
                    use_container_width=True
                )

                if submitted:
                    try:
                        add_availability(
                            employee_options[selected_employee],
                            str(selected_date),
                            availability_type,
                            reason
                        )

                        st.success("Availability record saved successfully!")
                        st.rerun()

                    except sqlite3.IntegrityError:
                        st.error(
                            "A record already exists for this employee on this date."
                        )

        else:
            st.info("No active employees available.")

    with tab2:
        st.subheader("Current Availability Records")

        if records:

            for record in records:
                with st.container(border=True):

                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.write(f"**{record[2]}** · {record[1]}")
                        st.write(
                            f"{record[3]}  |  {record[4]}"
                        )

                        if record[5]:
                            st.caption(f"Reason: {record[5]}")

                    with col2:
                        if st.button(
                            "Delete",
                            key=f"delete_availability_{record[0]}"
                        ):
                            delete_availability(record[0])
                            st.success("Record deleted.")
                            st.rerun()

        else:
            st.info("No availability records added yet.")


elif page == "Monthly Roster":

    st.title("Monthly Roster")
    st.caption("Generate, review and manage employee schedules.")

    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "Select Month",
            range(1, 13),
            format_func=lambda x: calendar.month_name[x],
            index=date.today().month - 1
        )

    with col2:
        selected_year = st.selectbox(
            "Select Year",
            range(date.today().year - 1, date.today().year + 3),
            index=1
        )

    st.divider()

    if st.button("Generate Monthly Roster", type="primary"):

        generate_month_roster(selected_year, selected_month)

        st.success("Monthly roster generated successfully!")
        st.rerun()

    records = get_month_roster(selected_year, selected_month)

    if records:

        working = sum(1 for r in records if r[7] == "Working")
        weekly_off = sum(1 for r in records if r[7] == "Weekly Off")
        leaves = sum(1 for r in records if r[7] == "Leave")
        unassigned = sum(1 for r in records if r[7] == "Unassigned")
        comp_off = sum(1 for r in records if r[7] == "Comp-Off")

        st.divider()
        st.subheader("Monthly Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Working Shifts", working)
        c2.metric("Weekly Offs", weekly_off)
        c3.metric("Leaves", leaves)
        c4.metric("Unassigned", unassigned)

        st.caption(f"Comp-Off records: {comp_off}")

        st.divider()

        tab1, tab2, tab3 = st.tabs([
            "Daily Roster",
            "Coverage Check",
            "Manual Edit"
        ])

        dates = sorted(set(r[1] for r in records))

        with tab1:

            selected_date = st.selectbox(
                "Select Date",
                dates
            )

            daily_records = [
                r for r in records if r[1] == selected_date
            ]

            for record in daily_records:

                with st.container(border=True):

                    st.write(f"**{record[3]}** · {record[2]}")
                    st.caption(f"Pod: {record[4]}")

                    if record[7] == "Working":
                        st.write(
                            f"{record[5]} / {record[6]}"
                        )
                    else:
                        st.write(f"Status: {record[7]}")

        with tab2:

            st.subheader("Process Coverage")

            processes = [
                p for p in get_processes() if p[4] == "Active"
            ]

            coverage_date = st.selectbox(
                "Choose date for coverage check",
                dates,
                key="coverage_date"
            )

            for process in processes:

                assigned_count = sum(
                    1 for r in records
                    if r[1] == coverage_date
                    and r[5] == process[1]
                    and r[6] == process[2]
                    and r[7] == "Working"
                )

                required = process[3]
                gap = max(0, required - assigned_count)

                st.write(
                    f"**{process[1]} / {process[2]}**"
                )

                st.write(
                    f"Required: {required} | "
                    f"Assigned: {assigned_count} | "
                    f"Gap: {gap}"
                )

                if gap > 0:
                    st.warning("Coverage requirement not met.")
                else:
                    st.success("Coverage requirement met.")

        with tab3:

            st.subheader("Manual Roster Edit")

            edit_date = st.selectbox(
                "Select Date",
                dates,
                key="edit_date"
            )

            edit_records = [
                r for r in records
                if r[1] == edit_date
            ]

            employee_options = {
                f"{r[3]} ({r[2]})": r
                for r in edit_records
            }

            selected_employee = st.selectbox(
                "Select Employee",
                list(employee_options.keys())
            )

            selected_record = employee_options[selected_employee]

            if selected_record[7] in [
                "Weekly Off", "Leave", "Comp-Off"
            ]:
                st.warning(
                    "This employee is unavailable on this date. "
                    "Change the availability record first."
                )

            else:

                employee_id = selected_record[2]

                employee_assignments = [
                    a for a in get_assignments()
                    if a[1] == employee_id
                ]

                process_options = {
                    f"{a[4]} / {a[5]}": a[3]
                    for a in employee_assignments
                }

                with st.form("manual_roster_form"):

                    new_status = st.selectbox(
                        "Roster Status",
                        ["Working", "Unassigned"]
                    )

                    new_process = None

                    if process_options:
                        selected_process = st.selectbox(
                            "Process",
                            list(process_options.keys())
                        )
                        new_process = process_options[selected_process]

                    save_edit = st.form_submit_button(
                        "Save Changes"
                    )

                    if save_edit:

                        if new_status == "Working" and not process_options:
                            st.error(
                                "This employee has no process assignment."
                            )

                        elif new_status == "Working":
                            update_roster_entry(
                                selected_record[0],
                                new_process,
                                "Working"
                            )
                            st.success("Roster updated.")
                            st.rerun()

                        else:
                            update_roster_entry(
                                selected_record[0],
                                None,
                                "Unassigned"
                            )
                            st.success("Roster updated.")
                            st.rerun()

    else:
        st.info(
            "No roster found for this month. "
            "Click Generate Monthly Roster to create one."
        )



elif page == "Conflict Detection":

    st.title("Conflict Detection")
    st.caption("Identify scheduling violations and workforce coverage issues.")

    st.divider()

    # ---------------- SELECT MONTH ----------------

    col1, col2 = st.columns(2)

    with col1:
        selected_month = st.selectbox(
            "Month",
            range(1, 13),
            index=date.today().month - 1,
            format_func=lambda m: calendar.month_name[m]
        )

    with col2:
        selected_year = st.number_input(
            "Year",
            min_value=2026,
            max_value=2035,
            value=date.today().year,
            step=1
        )

    roster = get_month_roster(
        int(selected_year),
        selected_month
    )

    st.divider()

    if not roster:
        st.warning(
            "No roster found for this month. "
            "Generate the roster from Monthly Roster first."
        )

    else:

        st.success(f"Roster loaded: {len(roster)} records.")

        availability_records = get_availability()
        processes = get_processes()
        employees = get_employees()

        # ---------------- LEAVE CONFLICTS ----------------

        st.subheader("1. Leave Conflicts")

        leave_dates = {
            (record[1], record[3])
            for record in availability_records
            if record[4] == "Leave"
        }

        leave_conflicts = [
            record for record in roster
            if (record[2], record[1]) in leave_dates
            and record[7] == "Working"
        ]

        if leave_conflicts:
            st.error(f"{len(leave_conflicts)} leave conflict(s) found.")

            for record in leave_conflicts:
                st.write(
                    f"**{record[3]}** ({record[2]}) — "
                    f"{record[1]} — {record[5]} / {record[6]}"
                )
        else:
            st.success("No leave conflicts found.")

        st.divider()

        # ---------------- WEEKLY OFF CONFLICTS ----------------

        st.subheader("2. Weekly Off Conflicts")

        weekly_off_dates = {
            (record[1], record[3])
            for record in availability_records
            if record[4] == "Weekly Off"
        }

        weekly_off_conflicts = [
            record for record in roster
            if record[7] == "Working"
            and (
                date.fromisoformat(record[1]).weekday() == 6
                or (record[2], record[1]) in weekly_off_dates
            )
        ]

        if weekly_off_conflicts:
            st.error(
                f"{len(weekly_off_conflicts)} weekly-off conflict(s) found."
            )

            for record in weekly_off_conflicts:
                st.write(
                    f"**{record[3]}** ({record[2]}) — "
                    f"{record[1]} — {record[5]} / {record[6]}"
                )
        else:
            st.success("No weekly-off conflicts found.")

        st.divider()

        # ---------------- COMP-OFF CONFLICTS ----------------

        st.subheader("3. Comp-Off Conflicts")

        comp_off_dates = {
            (record[1], record[3])
            for record in availability_records
            if record[4] == "Comp-Off"
        }

        comp_off_conflicts = [
            record for record in roster
            if (record[2], record[1]) in comp_off_dates
            and record[7] == "Working"
        ]

        if comp_off_conflicts:
            st.error(
                f"{len(comp_off_conflicts)} comp-off conflict(s) found."
            )

            for record in comp_off_conflicts:
                st.write(
                    f"**{record[3]}** ({record[2]}) — {record[1]}"
                )
        else:
            st.success("No comp-off conflicts found.")

        st.divider()

        # ---------------- COVERAGE GAPS ----------------

        st.subheader("4. Process Coverage Gaps")

        active_processes = [
            p for p in processes if p[4] == "Active"
        ]

        roster_dates = sorted(set(record[1] for record in roster))
        coverage_gaps = []

        for roster_date in roster_dates:

            # Sundays are weekly offs
            if date.fromisoformat(roster_date).weekday() == 6:
                continue

            for process in active_processes:

                brand_name = process[1]
                process_name = process[2]
                required = process[3]

                assigned = sum(
                    1 for record in roster
                    if record[1] == roster_date
                    and record[5] == brand_name
                    and record[6] == process_name
                    and record[7] == "Working"
                )

                if assigned < required:
                    coverage_gaps.append({
                        "date": roster_date,
                        "brand": brand_name,
                        "process": process_name,
                        "required": required,
                        "assigned": assigned,
                        "gap": required - assigned
                    })

        if coverage_gaps:
            st.error(f"{len(coverage_gaps)} coverage gap(s) found.")

            for gap in coverage_gaps:
                st.write(
                    f"**{gap['brand']} / {gap['process']}** — "
                    f"{gap['date']}"
                )
                st.write(
                    f"Required: {gap['required']} | "
                    f"Assigned: {gap['assigned']} | "
                    f"Shortage: {gap['gap']}"
                )
                st.divider()

        else:
            st.success("No process coverage gaps found.")

        st.divider()

        # ---------------- UNASSIGNED EMPLOYEES ----------------

        st.subheader("5. Unassigned Employees")

        unassigned_records = [
            record for record in roster
            if record[7] == "Unassigned"
        ]

        if unassigned_records:
            st.warning(
                f"{len(unassigned_records)} unassigned roster entries found."
            )

            for record in unassigned_records:
                st.write(
                    f"**{record[3]}** ({record[2]}) — {record[1]}"
                )
        else:
            st.success("No unassigned roster entries found.")

        st.divider()

        # ---------------- MISSING ROSTER ENTRIES ----------------

        st.subheader("6. Missing Roster Entries")

        active_employees = [
            emp for emp in employees if emp[5] == "Active"
        ]

        existing_entries = {
            (record[2], record[1])
            for record in roster
        }

        missing_entries = []

        for emp in active_employees:
            for roster_date in roster_dates:

                if (emp[0], roster_date) not in existing_entries:
                    missing_entries.append({
                        "name": emp[1],
                        "employee_id": emp[0],
                        "date": roster_date
                    })

        if missing_entries:
            st.error(
                f"{len(missing_entries)} missing roster entry(s) found."
            )

            for entry in missing_entries:
                st.write(
                    f"**{entry['name']}** ({entry['employee_id']}) — "
                    f"{entry['date']}"
                )
        else:
            st.success("No missing roster entries found.")

        # ---------------- VALIDATION SUMMARY ----------------

        st.divider()
        st.subheader("Validation Summary")

        total_issues = (
            len(leave_conflicts)
            + len(weekly_off_conflicts)
            + len(comp_off_conflicts)
            + len(coverage_gaps)
            + len(unassigned_records)
            + len(missing_entries)
        )

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Issues", total_issues)
        c2.metric("Scheduling Conflicts",
                  len(leave_conflicts)
                  + len(weekly_off_conflicts)
                  + len(comp_off_conflicts))
        c3.metric("Coverage Gaps", len(coverage_gaps))
