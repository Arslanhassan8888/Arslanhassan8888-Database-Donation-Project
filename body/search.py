# search.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module provides search functionality across the donation system.
It allows users to find records based on relationships between entities:
- Donations by donor, volunteer, event or beneficiary
- Events by volunteer participation
"""

from start.tables import get_connection

def fetch_all(query, param):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (param,))
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_all_donations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Donation")
    results = cursor.fetchall()
    conn.close()
    return results

def search_menu():
    while True:
        print("\n\033[92m--- Search Menu ---\033[0m", flush=True)

        print("\n\033[93mHere are all donations available in the system:\033[0m")
        donations = fetch_all_donations()
        if donations:
            for d in donations:
                print(
                    f"\033[92mID:\033[0m {d[0]}, "
                    f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                    f"\033[92mDate:\033[0m {d[2]}, "
                    f"\033[92mNotes:\033[0m {d[3]}, "
                    f"\033[92mDonor ID:\033[0m {d[4]}, "
                    f"\033[92mBeneficiary ID:\033[0m {d[5]}, "
                    f"\033[92mEvent ID:\033[0m {d[6]}, "
                    f"\033[92mVolunteer ID:\033[0m {d[7]}"
                )
        else:
            print("\033[93mNo donations available in the database.\033[0m")

        print("\n\033[92mChoose what to search by:\033[0m")
        print("1. Search Donations by Donor")
        print("2. Search Donations by Volunteer")
        print("3. Search Donations by Event")
        print("4. Search Events by Volunteer")
        print("5. Search Donations by Beneficiary")
        print("6. Back to Main Menu")

        choice = input("\033[92mChoose an option (1-6): \033[0m").strip()
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5", "6"]:
            print("\033[91mInvalid option. Please choose a number between 1 and 6.\033[0m")
            continue

        if choice == "1":
            search_donations("Donor", "Donor_ID", exclude=["Beneficiary_ID", "Event_ID", "Volunteer_ID"])
        elif choice == "2":
            search_donations("Volunteer", "Volunteer_ID", exclude=["Donor_ID", "Beneficiary_ID", "Event_ID"])
        elif choice == "3":
            search_donations("Event", "Event_ID", exclude=["Donor_ID", "Beneficiary_ID", "Volunteer_ID"])
        elif choice == "4":
            print("\n\033[93mTip: Volunteer ID must be numeric.\033[0m")
            volunteer_id = input("Enter Volunteer ID: ").strip()
            if not volunteer_id.isdigit():
                print("\033[91mVolunteer ID must be numeric.\033[0m")
                continue

            query = """
                SELECT e.* FROM Event e
                JOIN Volunteer v ON e.Event_ID = v.Event_ID
                WHERE v.Volunteer_ID = ?
            """
            events = fetch_all(query, volunteer_id)

            print("\n\033[92mEvents this volunteer is involved in:\033[0m")
            if events:
                for e in events:
                    print(
                        f"\033[92mID:\033[0m {e[0]}, "
                        f"\033[92mName:\033[0m {e[1]}, "
                        f"\033[92mDate:\033[0m {e[2]}, "
                        f"\033[92mLocation:\033[0m {e[3]}, "
                        f"\033[92mGoal:\033[0m £{e[4]:,.2f}, "
                        f"\033[92mDescription:\033[0m {e[5]}"
                    )
            else:
                print("\033[91mNo events found for this volunteer.\033[0m")
        elif choice == "5":
            search_donations("Beneficiary", "Beneficiary_ID", exclude=["Donor_ID", "Event_ID", "Volunteer_ID"])
        elif choice == "6":
            break

def search_donations(entity_name, column, exclude=None):
    exclude = exclude or []
    print(f"\n\033[93mTip: Enter a valid numeric ID for the selected {entity_name.lower()}\033[0m")
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
            output = [
                f"\033[92mID:\033[0m {d[0]}",
                f"\033[92mAmount:\033[0m £{d[1]:,.2f}",
                f"\033[92mDate:\033[0m {d[2]}",
                f"\033[92mNotes:\033[0m {d[3]}"
            ]
            if "Donor_ID" not in exclude:
                output.append(f"\033[92mDonor ID:\033[0m {d[4]}")
            if "Beneficiary_ID" not in exclude:
                output.append(f"\033[92mBeneficiary ID:\033[0m {d[5]}")
            if "Event_ID" not in exclude:
                output.append(f"\033[92mEvent ID:\033[0m {d[6]}")
            if "Volunteer_ID" not in exclude:
                output.append(f"\033[92mVolunteer ID:\033[0m {d[7]}")
            print(", ".join(output))
    else:
        print(f"\033[91mNo donations found for this {entity_name.lower()}.\033[0m")

if __name__ == "__main__":
    search_menu()
