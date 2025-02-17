from dotenv import dotenv_values
import streamlit as st
import mysql.connector
import datetime
from datetime import timedelta
from mysql.connector import OperationalError

# ---------- Helper Functions ----------
# Load credentials from .env file
cre = dotenv_values(r"credentials.env")

def get_connection():
    return mysql.connector.connect(
        host=cre['host'],
        database=cre['database'],
        user=cre['user'],
        password=cre['password'],
        autocommit=True,
        connection_timeout=600
    )

def run_query(query, params=None):
    """Execute a query and reconnect if necessary."""
    global conn, cursor
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
    except OperationalError as e:
        if e.errno == 2055:
            st.warning("Lost connection. Reconnecting...")
            conn = get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        else:
            raise
    return cursor

# ---------- Initialize Connection ----------
conn = get_connection()
cursor = conn.cursor()
st.set_page_config(page_title="Kira - Daily Progress Tracker", page_icon="kira_logo.png")  

st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #d3cce3, #e9e4f0);
            font-family: Arial, sans-serif;
        }
        .stTextInput>div>div>input {
            background-color: white;
            border-radius: 5px;
            border: 2px solid #4CAF50;
        }
        .task-label {
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        /* Radio button styling: We target the radio container class */
        .css-1wih3ys .stRadio > div {
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 4px;
            transition: background-color 0.3s ease;
        }
        .css-1wih3ys .stRadio > div:hover {
            background-color: #f1f1f1;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header Image and Title ----------
st.image("C:/Users/kiran/OneDrive/Desktop/TO-DO-TASK-Python/kid.jpg", use_container_width=True, caption="Stay Focused!")
st.title("Daily Progress Tracker")

# ---------- Define Today's Date ----------
# today_date = datetime.datetime.now().date()
today_date = datetime.date.today() 
today_day_name = today_date.strftime("%A")

# ---------- STEP 1: Fill in Missing Log Entries for Missed Days ----------
cursor.execute("SELECT MAX(task_date) FROM task_logs")
last_logged_row = cursor.fetchone()
last_logged_date = last_logged_row[0] if last_logged_row and last_logged_row[0] else None
if last_logged_date is None:
    last_logged_date = today_date - timedelta(days=1)

# For every day between (last_logged_date + 1) and (today_date - 1), fill in missing logs as Incomplete
missing_days = [last_logged_date + timedelta(days=i) for i in range(1, (today_date - last_logged_date).days)]
for missing_date in missing_days:
    active_tasks = run_query("SELECT task_id FROM tasks WHERE is_active = TRUE").fetchall()
    for (t_id,) in active_tasks:
        # Check if a log exists for this task on missing_date
        if not run_query("SELECT task_id FROM task_logs WHERE task_id = %s AND task_date = %s", (t_id, missing_date)).fetchone():
            week_number = f"Week {((missing_date.day - 1) // 7) + 1}"
            day_name = missing_date.strftime("%A")
            unique_task_number = f"TASK-{missing_date.strftime('%Y%m%d')}-{t_id}"
            run_query("""
                INSERT INTO task_logs (task_id, unique_task_number, week_number, day_name, task_date, task_time, is_completed)
                VALUES (%s, %s, %s, %s, %s, %s, 0)
            """, (t_id, unique_task_number, week_number, day_name, missing_date, datetime.datetime.now().time()))
            conn.commit()

# ---------- STEP 2: Display Statistics (Two Rows) ----------
total_tasks = run_query("SELECT COUNT(*) FROM tasks WHERE is_active = TRUE").fetchone()[0]
completed_today = run_query("SELECT COUNT(*) FROM task_logs WHERE task_date = %s AND is_completed = 1", (today_date,)).fetchone()[0]

target_date = datetime.date(2026,1,1)
days_left =  (target_date -  today_date).days

col_stat1, col_stat2 = st.columns(2)
with col_stat1:
    st.write(f"**📅 Date:** {today_date}")
    st.write(f"**📌 Day:** {today_day_name}")
with col_stat2:
    st.write(f"**✅ Total Tasks:** {total_tasks}")
    st.write(f"**🏆 Tasks Completed Today:** {completed_today}")
st.write(f"💀**Only {days_left} days remain until 2026**")


# ---------- STEP 3: New Task Input ----------
new_task = st.text_input("✍️ Enter new task:")
if st.button("➕ Add Task"):
    if new_task:
        if not run_query("SELECT task_id FROM tasks WHERE task_description = %s", (new_task,)).fetchone():
            run_query("INSERT INTO tasks (task_description) VALUES (%s)", (new_task,))
            conn.commit()
            st.success("Task added successfully!")
            st.rerun()
        else:
            st.warning("Task already exists!")
    else:
        st.error("Please enter a task description.")

# ---------- STEP 4: Display Active Tasks with Radio Button for Status (Auto-update) ----------
active_tasks = run_query("SELECT task_id, task_description FROM tasks WHERE is_active = TRUE").fetchall()

# Callback function for radio change
def update_status_callback(task_id, key, description):
    new_status = 1 if st.session_state[key] == "Completed" else 0
    current_time = datetime.datetime.now().time()
    unique_task_number = f"TASK-{today_date.strftime('%Y%m%d')}-{task_id}"
    week_number = f"Week {((today_date.day - 1) // 7) + 1}"
    try:
        run_query("""
            INSERT INTO task_logs (task_id, unique_task_number, week_number, day_name, task_date, task_time, is_completed)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (task_id, unique_task_number, week_number, today_day_name, today_date, current_time, new_status))
    except mysql.connector.IntegrityError:
        run_query("""
            UPDATE task_logs 
            SET is_completed = %s, task_time = %s 
            WHERE task_id = %s AND task_date = %s
        """, (new_status, current_time, task_id, today_date))
    conn.commit()
    st.success(f"Task '{description}' status updated!")

for task in active_tasks:
    task_id, description = task

    # Get today's log status; if missing, insert a default log (Incomplete)
    log_record = run_query("SELECT is_completed FROM task_logs WHERE task_id = %s AND task_date = %s", (task_id, today_date)).fetchone()
    current_status = log_record[0] if log_record else 0
    if not log_record:
        week_number = f"Week {((today_date.day - 1) // 7) + 1}"
        unique_task_number = f"TASK-{today_date.strftime('%Y%m%d')}-{task_id}"
        run_query("""
            INSERT INTO task_logs (task_id, unique_task_number, week_number, day_name, task_date, task_time, is_completed)
            VALUES (%s, %s, %s, %s, %s, %s, 0)
        """, (task_id, unique_task_number, week_number, today_day_name, today_date, datetime.datetime.now().time()))
        conn.commit()
        current_status = 0

    col1, col2, col3 = st.columns([4, 2, 1])
    with col1:
        st.markdown(f"<p class='task-label'>{description}</p>", unsafe_allow_html=True)
    key_name = f"status_{task_id}"
    with col2:
        st.radio(
            "",
            options=["Not Completed", "Completed"],
            index=current_status,
            key=key_name,
            label_visibility="collapsed",
            on_change=update_status_callback,
            args=(task_id, key_name, description)
        )
    with col3:
        if st.button("🗑️ Remove", key=f"del_{task_id}"):
            run_query("DELETE FROM tasks WHERE task_id = %s", (task_id,))
            conn.commit()
            st.warning(f"Task '{description}' removed!")
            st.rerun()

# ---------- STEP 5: Close the Database Connection ----------
conn.close()
