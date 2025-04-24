# values.py
from start.tables import get_connection
"""
This module provides sample data for the donation management system.
It contains a single function that insert values in all database tables that can be used for testing and demostration
Clears all existing data and inserts fresh sample records into all tables.
The data represents a typical set of records for a charity organisation.

UPDATED: With ON DELETE CASCADE enabled, deletion order is less critical, but we still clear in dependency-safe order.
"""

def insert_sample_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear tables /
    # Clear all existing data from tables (in reverse order of foreign key dependencies)
    # With ON DELETE CASCADE, child rows will auto-delete, but we do this explicitly for clean setup

    cursor.execute("DELETE FROM Donation")
    cursor.execute("DELETE FROM Volunteer")
    cursor.execute("DELETE FROM Event")
    cursor.execute("DELETE FROM Beneficiary")
    cursor.execute("DELETE FROM Donor")

    # Donors
    cursor.execute("INSERT INTO Donor (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth) VALUES ('John', 'Doe', 'john@example.com', '123456789', '123 Main St', '1980-01-01')")
    cursor.execute("INSERT INTO Donor (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth) VALUES ('Jane', 'Smith', 'jane@another.com', '987654321', '456 Oak Ave', '1992-03-15')")
    cursor.execute("INSERT INTO Donor (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth) VALUES ('Peter', 'Jones', 'peter@third.org', '1122334455', '789 Pine Rd', '1975-11-22')")
    cursor.execute("INSERT INTO Donor (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth) VALUES ('Susan', 'Davis', 'susan@fourth.net', '9988776655', '333 Lake Rd', '1988-06-30')")

    # Beneficiaries
    cursor.execute("INSERT INTO Beneficiary (Name, Type, Address, Support_Duration, Funding_priority) VALUES ('Children Foundation', 'Charity', '456 Oak Ave', '5 years', 'High')")
    cursor.execute("INSERT INTO Beneficiary (Name, Type, Address, Support_Duration, Funding_priority) VALUES ('Elderly Support', 'Non-Profit', '10 Downing St', 'Ongoing', 'Medium')")
    cursor.execute("INSERT INTO Beneficiary (Name, Type, Address, Support_Duration, Funding_priority) VALUES ('Animal Shelter', 'Charity', '221B Baker St', '3 years', 'High')")
    cursor.execute("INSERT INTO Beneficiary (Name, Type, Address, Support_Duration, Funding_priority) VALUES ('Environmental Fund', 'Charity', '77 Green Way', 'Permanent', 'Medium')")

    # Events
    cursor.execute("INSERT INTO Event (Name, Date, Location, Fundraising_Goal, Description) VALUES ('Gala Dinner', '2025-12-15', 'Grand Hall', 15000.0, 'Annual fundraising event')")
    cursor.execute("INSERT INTO Event (Name, Date, Location, Fundraising_Goal, Description) VALUES ('Marathon Run', '2025-11-20', 'City Park', 20000.0, 'Charity marathon')")
    cursor.execute("INSERT INTO Event (Name, Date, Location, Fundraising_Goal, Description) VALUES ('Bake Sale', '2025-10-01', 'Town Square', 1000.0, 'Community bake sale')")
    cursor.execute("INSERT INTO Event (Name, Date, Location, Fundraising_Goal, Description) VALUES ('Art Auction', '2026-03-10', 'Gallery One', 12000.0, 'Fundraiser for local artists')")

    # Volunteers
    cursor.execute("INSERT INTO Volunteer (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth, Event_ID) VALUES ('Alice', 'Brown', 'alice@volunteer.net', '555123456', '321 Elm St', '2000-07-10', 1)")
    cursor.execute("INSERT INTO Volunteer (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth, Event_ID) VALUES ('Bob', 'Green', 'bob@helper.com', '666987654', '654 Willow Dr', '1998-09-03', 2)")
    cursor.execute("INSERT INTO Volunteer (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth, Event_ID) VALUES ('Charlie', 'White', 'charlie@assist.org', '777112233', '987 Maple Ln', '2002-04-18', 3)")
    cursor.execute("INSERT INTO Volunteer (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth, Event_ID) VALUES ('Diana', 'Black', 'diana@serve.org', '888445566', '11 Oak Ct', '1995-12-25', 4)")

    # Donations
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Beneficiary_ID, Event_ID, Volunteer_ID) VALUES (500.0, '2025-11-01', 'John to Children Foundation', 1, 1, 1, 1)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Beneficiary_ID, Event_ID, Volunteer_ID) VALUES (350.0, '2025-11-03', 'John to Elderly Support', 1, 2, 2, 2)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Beneficiary_ID, Event_ID, Volunteer_ID) VALUES (200.0, '2025-11-05', 'Jane to Animal Shelter', 2, 3, 3, 3)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Beneficiary_ID, Event_ID, Volunteer_ID) VALUES (180.0, '2025-11-06', 'Peter to Environmental Fund', 3, 4, 4, 4)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Beneficiary_ID, Event_ID, Volunteer_ID) VALUES (120.0, '2025-11-07', 'Susan to Children Foundation', 4, 1, 1, 1)")

    conn.commit()
    conn.close()
