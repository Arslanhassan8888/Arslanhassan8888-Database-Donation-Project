"""
This module contains basic CRUD (Create, Read, Update, Delete) operations
for interacting with the database. These functions are used throughout
the application to manage data in the SQLite database.
"""
from start.tables import get_connection

"""
This function retrieves all records from a specified database table.
Parameters:
    table (str): The name of the table to query
Returns:
    list: All records from the table as a list of tuples
"""
def view_all(table):
    conn = get_connection() # Establish connection to the database
    cursor = conn.cursor() # Create a cursor object to execute SQL commands
    cursor.execute(f"SELECT * FROM {table}") # Execute SQL query to select all records from the table
    results = cursor.fetchall() # Fetch all results from the query
    conn.close() # Always close the connection
    return results

"""
This function adds a new record to the database.
Parameters:
    query (str): SQL INSERT statement with placeholders
    values (tuple): Values to insert into the placeholders
"""
def add_entry(query, values):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values) # Execute the insert query with provided values
    conn.commit()
    conn.close()

"""
This function updates existing records in the database.
Parameters:
    query (str): SQL UPDATE statement with placeholders
    values (tuple): New values for the record including ID

Note: The values tuple must include the record ID as the last element for the WHERE clause in the UPDATE statement
"""
def update_entry(query, values):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    conn.close()

"""
This function deletes a record from the database.
Parameters: 
    query (str): SQL DELETE statement with placeholder
    id (int/str): The ID of the record to delete

UPDATED: With ON DELETE CASCADE enabled in table.py, this now automatically deletes related records
(e.g., donations) without manual checks in the interface modules.
"""
def delete_entry(query, id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (id,)) # Execute delete with the provided ID
    conn.commit()
    conn.close()

"""
This function checks if a record (Donor, Event, Business, Beneficiary) has linked donations.
Parameters:
    column (str): The column to check (e.g., 'Donor_ID', 'Event_ID', 'Business_ID', 'Beneficiary_ID')
    id (int/str): The ID of the record to check
Returns:
     True if linked donations exist, False otherwise
"""
def has_linked_donations(column, id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM Donation WHERE {column} = ?", (id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None
