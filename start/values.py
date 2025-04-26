# values.py
from start.tables import get_connection

"""
This module provides sample data for the donation management system.
It contains a single function that insert values in all database tables that can be used for testing and demonstration.
Clears all existing data and inserts fresh sample records into all tables.
The data represents a typical set of records for a charity organization.

UPDATED: With correct Business columns and correct Donation relationships.
"""

def insert_sample_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Clear tables
    cursor.execute("DELETE FROM Donation")
    cursor.execute("DELETE FROM Business")
    cursor.execute("DELETE FROM Event")
    cursor.execute("DELETE FROM Beneficiary")
    cursor.execute("DELETE FROM Donor")

    # Insert Donors
    cursor.execute("INSERT INTO Donor (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth) VALUES ('John', 'Doe', 'john@example.com', '123456789', '123 Main St', '1980-01-01')")
    cursor.execute("INSERT INTO Donor (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth) VALUES ('Jane', 'Smith', 'jane@another.com', '987654321', '456 Oak Ave', '1992-03-15')")
    cursor.execute("INSERT INTO Donor (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth) VALUES ('Peter', 'Jones', 'peter@third.org', '1122334455', '789 Pine Rd', '1975-11-22')")
    cursor.execute("INSERT INTO Donor (First_Name, Last_Name, Email, Phone_Number, Address, Date_of_Birth) VALUES ('Susan', 'Davis', 'susan@fourth.net', '9988776655', '333 Lake Rd', '1988-06-30')")

    # Insert Beneficiaries
    cursor.execute("INSERT INTO Beneficiary (Name, Type, Address, Support_Duration, Funding_priority) VALUES ('Children Foundation', 'Charity', '456 Oak Ave', '5 years', 'High')")
    cursor.execute("INSERT INTO Beneficiary (Name, Type, Address, Support_Duration, Funding_priority) VALUES ('Elderly Support', 'Non-Profit', '10 Downing St', 'Ongoing', 'Medium')")
    cursor.execute("INSERT INTO Beneficiary (Name, Type, Address, Support_Duration, Funding_priority) VALUES ('Animal Shelter', 'Charity', '221B Baker St', '3 years', 'High')")
    cursor.execute("INSERT INTO Beneficiary (Name, Type, Address, Support_Duration, Funding_priority) VALUES ('Environmental Fund', 'Charity', '77 Green Way', 'Permanent', 'Medium')")

    # Insert Events
    cursor.execute("INSERT INTO Event (Name, Date, Location, Fundraising_Goal, Description) VALUES ('Gala Dinner', '2025-12-15', 'Grand Hall', 15000.0, 'Annual fundraising event')")
    cursor.execute("INSERT INTO Event (Name, Date, Location, Fundraising_Goal, Description) VALUES ('Marathon Run', '2025-11-20', 'City Park', 20000.0, 'Charity marathon')")
    cursor.execute("INSERT INTO Event (Name, Date, Location, Fundraising_Goal, Description) VALUES ('Bake Sale', '2025-10-01', 'Town Square', 1000.0, 'Community bake sale')")
    cursor.execute("INSERT INTO Event (Name, Date, Location, Fundraising_Goal, Description) VALUES ('Art Auction', '2026-03-10', 'Gallery One', 12000.0, 'Fundraiser for local artists')")

    # Insert Businesses 
    cursor.execute("INSERT INTO Business (Name, Email, Phone_Number, Address, Registration_Date) VALUES ('TechCorp', 'contact@techcorp.com', '111111111', '123 Silicon Valley', '2024-01-01')")
    cursor.execute("INSERT INTO Business (Name, Email, Phone_Number, Address, Registration_Date) VALUES ('GreenEnergy', 'info@greenenergy.com', '222222222', '456 Green Street', '2023-06-10')")
    cursor.execute("INSERT INTO Business (Name, Email, Phone_Number, Address, Registration_Date) VALUES ('FoodiesHub', 'support@foodieshub.com', '333333333', '789 Food Plaza', '2022-11-15')")
    cursor.execute("INSERT INTO Business (Name, Email, Phone_Number, Address, Registration_Date) VALUES ('EduWorld', 'hello@eduworld.com', '444444444', '101 Learning Blvd', '2021-08-20')")

    # Insert Donations
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) VALUES (500.0, '2025-11-01', 'John donates to Children Foundation', 1, NULL, NULL, 1)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) VALUES (350.0, '2025-11-03', 'John donates to Elderly Support', 1, NULL, NULL, 2)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) VALUES (200.0, '2025-11-05', 'Jane donates to Animal Shelter', 2, NULL, NULL, 3)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) VALUES (1000.0, '2025-12-20', 'Event Gala Dinner for Environmental Fund', NULL, 1, NULL, 4)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) VALUES (800.0, '2025-11-22', 'Event Marathon Run for Elderly Support', NULL, 2, NULL, 2)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) VALUES (750.0, '2025-12-01', 'TechCorp donates to Children Foundation', NULL, NULL, 1, 1)")
    cursor.execute("INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) VALUES (600.0, '2025-11-18', 'GreenEnergy donation to Environmental Fund', NULL, NULL, 2, 4)")

    conn.commit()
    conn.close()
