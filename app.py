import streamlit as st
import sqlite3

st.title("⚡ SimuGrid Test Dashboard")

# READ SECRETS
db_file = st.secrets["database"]["db_name"]

# 🛠️ CLOUD INITIALIZATION BLOCK
# This runs every time the app starts to guarantee the database structure exists
def init_db():
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    # Create table if missing
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS substations (
        substation_id TEXT PRIMARY KEY,
        substation_name TEXT,
        status TEXT
    );
    """)
    # Insert starter data if the table is completely empty
    cursor.execute("SELECT COUNT(*) FROM substations")
    if cursor.fetchone()[0] == 0:
        test_rows = [
            ('1', 'North Grid', 'Active'),
            ('2', 'South Station', 'Maintenance')
        ]
        cursor.executemany("""
        INSERT INTO substations (substation_id, substation_name, status)
        VALUES (?, ?, ?);
        """, test_rows)
        connection.commit()
    connection.close()

# Run the initialization
init_db()

# Create layout panes (Sidebar and Main View)
sidebar_pane, main_pane = st.columns([1, 2])

# Control Pane layout with a visible border
with sidebar_pane:
    with st.container(border=True):
        st.header("📁 Controls")
        substation_id = st.text_input("Enter Substation ID:")
        fetch_button = st.button("Fetch Status")

# Visualization Pane layout with a visible border
with main_pane:
    with st.container(border=True):
        st.header("🗺️ Grid Visualization")
        status_box = st.empty()

        if fetch_button:
            # Validation Guard Check
            if substation_id.strip():
                # 1. Connect to the database file
                # OLD WAY (Hardcoded/Insecure):
                # connection = sqlite3.connect("simugrid.db")

                # NEW WAY (Secure/Dynamic):
                db_file = st.secrets["database"]["db_name"]
                connection = sqlite3.connect(db_file)
                cursor = connection.cursor()
                
                # 2. Run a secure parameterized query
                query = "SELECT substation_name, status FROM substations WHERE substation_id = ?"
                cursor.execute(query, (substation_id.strip(),))
                
                row = cursor.fetchone()
                connection.close()
                
                # 3. Render the output to our layout placeholder
                if row:
                    name, status = row[0], row[1]
                    status_box.success(f"📍 {name} | Status: {status}")
                else:
                    status_box.error(f"❌ Substation ID '{substation_id}' not found.")
            else:
                status_box.error("⚠️ Please enter an ID first.")