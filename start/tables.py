# Updated table.py
# Import the sqlite3 module and give it a short name 'db', this is like an alias
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
# UPDATED: Added ON DELETE CASCADE to all foreign key constraints
# This ensures related records are automatically deleted when a parent is removed

def create_tables():
    conn = get_connection()  # Start the connection to the database
    cursor = conn.cursor()   # Get a cursor, used to run SQL commands. Acts as a bridge between Python and DB

    # Below, we run several SQL commands in one go using executescript()
    cursor.executescript("""
    -- First, remove all old versions of the tables if they are there
    DROP TABLE IF EXISTS Donation;
    DROP TABLE IF EXISTS Volunteer;
    DROP TABLE IF EXISTS Event;
    DROP TABLE IF EXISTS Beneficiary;
    DROP TABLE IF EXISTS Donor;

    /*
    Create the Donor table.
    Stores people who give money.
    Email and phone must be unique and names can't be blank.
    */
    CREATE TABLE Donor (
        Donor_ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- A unique ID given by the system
        First_Name TEXT NOT NULL,                    -- First name is needed
        Last_Name TEXT NOT NULL,                     -- Last name is needed
        Email TEXT NOT NULL UNIQUE,                  -- Email must be unique and not empty
        Phone_Number INTEGER NOT NULL UNIQUE,        -- Phone must be unique and numeric
        Address TEXT,                                -- Optional address
        Date_of_Birth TEXT NOT NULL                  -- Date of birth in format YYYY-MM-DD
    );

    CREATE TABLE Beneficiary (
        Beneficiary_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Type TEXT NOT NULL,
        Address TEXT,                      -- Optional address
        Support_Duration TEXT,
        Funding_priority TEXT
    );

    CREATE TABLE Event (
        Event_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Date TEXT NOT NULL,
        Location TEXT,
        Fundraising_Goal REAL,
        Description TEXT
    );

    CREATE TABLE Volunteer (
        Volunteer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        First_Name TEXT NOT NULL,
        Last_Name TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,             -- Email must be unique
        Phone_Number INTEGER NOT NULL UNIQUE,   -- Phone must be unique
        Address TEXT,                           -- Optional address
        Date_of_Birth TEXT NOT NULL,
        Event_ID INTEGER NOT NULL,
        FOREIGN KEY(Event_ID) REFERENCES Event(Event_ID) ON DELETE CASCADE
    );

    CREATE TABLE Donation (
        Donation_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Amount REAL NOT NULL,
        Date TEXT NOT NULL,
        Notes TEXT,
        Donor_ID INTEGER,
        Beneficiary_ID INTEGER,
        Event_ID INTEGER,
        Volunteer_ID INTEGER,
        FOREIGN KEY(Donor_ID) REFERENCES Donor(Donor_ID) ON DELETE CASCADE,
        FOREIGN KEY(Beneficiary_ID) REFERENCES Beneficiary(Beneficiary_ID) ON DELETE CASCADE,
        FOREIGN KEY(Event_ID) REFERENCES Event(Event_ID) ON DELETE CASCADE,
        FOREIGN KEY(Volunteer_ID) REFERENCES Volunteer(Volunteer_ID) ON DELETE CASCADE
    );
    """)

    conn.commit()  # Save the changes to the database
    conn.close()   # Close the database connection
