# tables.py
# Import the sqlite3 module and give it a short name 'db', this like an alias
# It is used to communicate with the database
import sqlite3 as db

# A small function to open a connection to the database file. This file holds all our data
# IMPORTANT: Enabling foreign key support on every connection
# This ensures cascading deletions are enforced by SQLite
def get_connection():
    conn = db.connect("donation_app.db")  # Connect to the SQLite database file
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
    return conn

# This function creates all the tables we need for the app
def create_tables():
    conn = get_connection()  # Start the connection to the database
    cursor = conn.cursor()   # Get a cursor, used to run SQL commands. Acts as a bridge between Python and DB

    # Run several SQL commands in one go using executescript()
    cursor.executescript("""
    -- First, remove all old versions of the tables if they are there
    DROP TABLE IF EXISTS Donation;
    DROP TABLE IF EXISTS Volunteer; -- Drop Volunteer first (new subtable linked to Event)
    DROP TABLE IF EXISTS Business;
    DROP TABLE IF EXISTS Event;
    DROP TABLE IF EXISTS Beneficiary;
    DROP TABLE IF EXISTS Donor;

    /*
    Create the Donor table.
    NOT NULL constraints ensure that all fields are filled in.
    Unique constraints ensure that no two donors can have the same email or phone number.
    */
    CREATE TABLE Donor (
        Donor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_Name TEXT NOT NULL,
        Last_Name TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Phone_Number INTEGER NOT NULL UNIQUE,
        Address TEXT,
        Date_of_Birth TEXT NOT NULL
    );

    /*
    Create the Beneficiary table.
    Stores organisations or individuals who receive support.
    */
    CREATE TABLE Beneficiary (
        Beneficiary_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Type TEXT NOT NULL,
        Address TEXT,
        Support_Duration TEXT,
        Funding_priority TEXT
    );

    /*
    Create the Event table.
    Stores information about fundraising events.
    */
    CREATE TABLE Event (
        Event_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Date TEXT NOT NULL,
        Location TEXT,
        Fundraising_Goal REAL,
        Description TEXT
    );

    /*
    Create the Business table.
    Stores information about businesses that participate in donations.
    */
    CREATE TABLE Business (
        Business_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        Phone_Number INTEGER NOT NULL UNIQUE,
        Address TEXT,
        Registration_Date TEXT NOT NULL
    );

    /*
    Create the Volunteer table.
    Stores volunteers linked to specific events.
    One event can have many volunteers.
    */
    CREATE TABLE Volunteer (
        Volunteer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Event_ID INTEGER NOT NULL,
        First_Name TEXT NOT NULL,
        Last_Name TEXT NOT NULL,
        Address TEXT,
        Date_of_Birth TEXT,
        Contact_Number TEXT,
        FOREIGN KEY(Event_ID) REFERENCES Event(Event_ID) ON DELETE CASCADE
    );

    /*
    Create the Donation table.
    Each donation is always linked to:
    - Exactly one Beneficiary (mandatory)
    - And exactly one source: Donor OR Event OR Business
    */
    CREATE TABLE Donation (
        Donation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Amount REAL NOT NULL,
        Date TEXT NOT NULL,
        Notes TEXT,
        Donor_ID INTEGER,
        Event_ID INTEGER,
        Business_ID INTEGER,
        Beneficiary_ID INTEGER NOT NULL,
        FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID),
        FOREIGN KEY(Event_ID) REFERENCES Event(Event_ID),
        FOREIGN KEY(Business_ID) REFERENCES Business(Business_ID),
        FOREIGN KEY(Beneficiary_ID) REFERENCES Beneficiary(Beneficiary_ID)
    );
    """)

    conn.commit()  # Save the changes to the database
    conn.close()   # Close the database connection
