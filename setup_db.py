import sqlite3

# 1. Connect to SQLite (this will automatically create a file named 'simugrid.db')
connection = sqlite3.connect("simugrid.db")
cursor = connection.cursor()

# 2. Create the spreadsheet structure (Schema)
cursor.execute("""
CREATE TABLE IF NOT EXISTS substations (
    substation_id TEXT PRIMARY KEY,
    substation_name TEXT,
    status TEXT
);
""")

# 3. Insert our initial test data rows safely
test_rows = [
    ('1', 'North Grid', 'Active'),
    ('2', 'South Station', 'Maintenance')
]

# Use executemany with placeholders (?) to prevent SQL injection
cursor.executemany("""
INSERT OR REPLACE INTO substations (substation_id, substation_name, status)
VALUES (?, ?, ?);
""", test_rows)

# 4. Save changes and close the connection
connection.commit()
connection.close()

print("Database 'simugrid.db' successfully created with test rows!")