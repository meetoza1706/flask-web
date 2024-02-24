import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SQL query to select all records from a table
cursor.execute('SELECT * FROM data')

# Fetch all rows from the result set
rows = cursor.fetchall()

# Print the rows (or process them as needed)
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
