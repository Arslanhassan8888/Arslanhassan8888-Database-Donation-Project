"""
This module contains basic CRUD (Create, Read, Update, Delete) operations
for interacting with the database. These functions are used throughout
the application to manage data in the SQLite database.

IMPORTANT: These functions assume all input validation has been done by the calling code.
They focus solely on database operations and will propagate any database errors.
"""

from start.tables import get_connection

def _execute_operation(query, params=None, fetch=False):
    """
    Internal helper function to execute database operations.
    Parameters:
        query (str): SQL query to execute
        params (tuple/None): Parameters for the query
        fetch (bool): Whether to fetch results
    Returns:
        list: Results if fetch=True, None otherwise
    Raises:
        sqlite3.Error: For any database-related errors
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
    finally:
        conn.close()

"""
Retrieves all records from a specified table.
Parameters:
    table (str): Name of the table to query
Returns:
    list: All records as list of tuples
Raises:
    sqlite3.Error: If table doesn't exist or query fails
"""
def view_all(table):
    return _execute_operation(f"SELECT * FROM {table}", fetch=True)

"""
Adds a new record to the database.
Parameters:
    query (str): SQL INSERT statement with placeholders
    values (tuple): Values for the placeholders
Raises:
    sqlite3.Error: If insertion fails (constraint violation, etc.)
"""
def add_entry(query, values):
    _execute_operation(query, values)

"""
Updates existing records in the database.
Parameters:
    query (str): SQL UPDATE statement with placeholders
    values (tuple): New values including ID for WHERE clause
Raises:
    sqlite3.Error: If update fails or record doesn't exist
"""
def update_entry(query, values):
    _execute_operation(query, values)

"""
Deletes a record from the database.
Parameters:
    query (str): SQL DELETE statement with placeholder
    id (int/str): ID of the record to delete
Raises:
    sqlite3.Error: If deletion fails
Note:
    ON DELETE CASCADE in tables.py handles related records automatically
"""
def delete_entry(query, id):
    _execute_operation(query, (id,))

"""
Checks if a record has linked donations.
Parameters:
    column (str): Column name to check (e.g., 'Donor_ID')
    id (int/str): ID of the record to check
Returns:
    bool: True if linked donations exist, False otherwise
Raises:
    sqlite3.Error: If query fails
"""
def linked_donations(column, id):
    result = _execute_operation(
        f"SELECT 1 FROM Donation WHERE {column} = ?", 
        (id,), 
        fetch=True
    )
    return bool(result)

"""
Checks if an event has linked volunteers.
Parameters:
    event_id (int/str): ID of the event to check
Returns:
    bool: True if volunteers exist, False otherwise
Raises:
    sqlite3.Error: If query fails
"""
def linked_volunteers(event_id):
    result = _execute_operation(
        "SELECT 1 FROM Volunteer WHERE Event_ID = ?",
        (event_id,),
        fetch=True
    )
    return bool(result)
