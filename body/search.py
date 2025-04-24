# search.py
"""
This module provides search functionality across the donation system.
It allows users to find records based on relationships between entities:
- Donations by donor, volunteer, event or beneficiary
- Events by volunteer participation
"""

from start.tables import get_connection

# This helper function runs a SQL query and returns all matching results
# No changes needed here for cascade functionality, but added comment for clarity

def fetch_all(query, param):
    conn = get_connection()  # Establish database connection
    cursor = conn.cursor()   # Create cursor for executing SQL
    cursor.execute(query, (param,))  # Execute query with parameter
    results = cursor.fetchall()      # Get all matching records
    conn.close()            # Close connection
    return results

def search_menu():
    while True:
        # Display search options with green header
        print("\n\033[92m--- Search Menu ---\033[0m", flush=True)
        print("1. Search Donations by Donor")
        print("2. Search Donations by Volunteer")
        print("3. Search Donations by Event")
        print("4. Search Events by Volunteer")
        print("5. Search Donations by Beneficiary")
        print("6. Back to Main Menu")

        # Get and validate user choice
        choice = input("\033[92mChoose an option (1-6): \033[0m").strip()
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5", "6"]:
            print("\033[91mInvalid option. Please choose a number between 1 and 6.\033[0m")
            continue

        # Option 1: Search donations by donor
        if choice == "1":
            search_donations("Donor", "Donor_ID")

        # Option 2: Search donations by volunteer
        elif choice == "2":
            search_donations("Volunteer", "Volunteer_ID")

        # Option 3: Search donations by event
        elif choice == "3":
            search_donations("Event", "Event_ID")

        # Option 4: Search events by volunteer participation
        elif choice == "4":
            volunteer_id = input("Enter Volunteer ID: ").strip()
            if not volunteer_id.isdigit():
                print("\033[91mVolunteer ID must be numeric.\033[0m")
                continue

            # Query to find events a volunteer is associated with
            query = """
                SELECT e.* FROM Event e
                JOIN Volunteer v ON e.Event_ID = v.Event_ID
                WHERE v.Volunteer_ID = ?
            """
            events = fetch_all(query, volunteer_id)

            # Display results
            print("\n\033[92mEvents this volunteer is involved in:\033[0m")
            if events:
                for e in events:
                    print(
                        f"\033[92mName:\033[0m {e[1]}, "
                        f"\033[92mDate:\033[0m {e[2]}, "
                        f"\033[92mLocation:\033[0m {e[3]}, "
                        f"\033[92mGoal:\033[0m £{e[4]:,.2f}, "
                        f"\033[92mDescription:\033[0m {e[5]}"
                    )
            else:
                print("\033[91mNo events found for this volunteer.\033[0m")

        # Option 5: Search donations by beneficiary
        elif choice == "5":
            search_donations("Beneficiary", "Beneficiary_ID")

        # Option 6: Exit to main menu
        elif choice == "6":
            break

"""
Generic function to search donations by related entity.
Parameters:
    entity_name - Human-readable name (Donor/Volunteer/etc)
    column - Database column to search against
No changes required here either. Cascade deletions remove irrelevant records, so only valid results will show.
"""
def search_donations(entity_name, column):
    entity_id = input(f"Enter {entity_name} ID: ").strip()
    if not entity_id.isdigit():
        print(f"\033[91m{entity_name} ID must be numeric.\033[0m")
        return

    donations = fetch_all(
        f"SELECT * FROM Donation WHERE {column} = ?",
        entity_id
    )

    print(f"\n\033[92mDonations related to this {entity_name.lower()}:\033[0m")
    if donations:
        for d in donations:
            print(
                f"\033[92mID:\033[0m {d[0]}, "
                f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                f"\033[92mDate:\033[0m {d[2]}, "
                f"\033[92mNotes:\033[0m {d[3]}"
            )
    else:
        print(f"\033[91mNo donations found for this {entity_name.lower()}.\033[0m")

if __name__ == "__main__":
    search_menu()
