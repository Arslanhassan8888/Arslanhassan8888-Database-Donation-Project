from functions import create_table, insert_rows

drop_event = "DROP TABLE IF EXISTS Event"
create_event = """
CREATE TABLE IF NOT EXISTS Event (
    Event_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE,
    Date TEXT NOT NULL,
    Location TEXT NOT NULL,
    Fundraising_Goal REAL DEFAULT 0.0 CHECK(Fundraising_Goal >= 0),
    Description TEXT
)
"""
events = [
    (1, 'Charity Run', '2024-08-01', 'Hyde Park, London', 5000.0, 'Annual 5K charity run'),
    (2, 'Gala Dinner', '2024-09-15', 'The Ritz, London', 10000.0, 'Formal fundraising dinner'),
    (3, 'Bake Sale', '2024-05-20', 'Community Hall, Manchester', 1200.0, 'Homemade goods fundraising'),
    (4, 'School Fair', '2024-06-10', 'Greenhill Primary, Birmingham', 3000.0, 'School fundraising event'),
    (5, 'Music Concert', '2024-07-12', 'O2 Academy, Glasgow', 7500.0, 'Benefit concert for youth programs'),
    (6, 'Book Drive', '2024-10-05', 'City Library, Leeds', 800.0, 'Collecting books for education'),
]
insert_event = "INSERT INTO Event VALUES (?, ?, ?, ?, ?, ?)"

def event_setup(connection, drop=True):
    create_table(connection, create_event, drop_event if drop else None)
    insert_rows(connection, insert_event, events)