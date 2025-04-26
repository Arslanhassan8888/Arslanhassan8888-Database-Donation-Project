# search.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module provides search functionality across the donation system.
It allows users to find records based on relationships between entities:
- Donations by donor, event, business, or beneficiary
"""

from start.tables import get_connection

# Fetch query results based on parameter
def fetch_all(query, param):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (param,))# Fetch all results 
    results = cursor.fetchall() #  matching the query with parameter
    conn.commit() 
    conn.close()
    return results 

def fetch_all_donations(): # Fetch all donations from the database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Donation") # Execute SQL query to select all donations matching the query with parameter
    results = cursor.fetchall()
    conn.close()
    return results 

def search_menu():
    while True:
        # Print menu options with decoration
        print("\n" + "🔎  SEARCH MANAGEMENT MENU  🔍".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  Search Donations by Donor")
        print("2️⃣  Search Donations by Event")
        print("3️⃣  Search Donations by Business")
        print("4️⃣  Search Donations by Beneficiary")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n🌟 Choose an option (1-5): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91m🚫 Invalid option. Please choose a number between 1 and 5.\033[0m")
            continue

        # Fetch and display all donations
        if choice in ["1", "2", "3", "4"]:
            print("\n\033[92mHere are all donations available:\033[0m")
            donations = fetch_all_donations()
            if donations:
                for d in donations:
                    print(
                        f"\033[92mID:\033[0m {d[0]}, "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f}, " 
                        f"\033[92mDate:\033[0m {d[2]}, "
                        f"\033[92mNotes:\033[0m {d[3]}, "
                        f"\033[92mDonor ID:\033[0m {d[4]}, "
                        f"\033[92mEvent ID:\033[0m {d[5]}, "
                        f"\033[92mBusiness ID:\033[0m {d[6]}, "
                        f"\033[92mBeneficiary ID:\033[0m {d[7]}"
                    )
            else:
                print("\033[93mNo donations available in the database.\033[0m")

        if choice == "1":
            # Search Donations by Donor
            print("\n\033[93mTip: Insert a Donor ID to search related donations.\033[0m")
            donor_id = input("Enter Donor ID: ").strip()
            if not donor_id.isdigit():
                print("\033[91m🚫 Donor ID must be numeric.\033[0m")
                continue

            donations = fetch_all( # Fetch all donations from the database  Execute SQL query to select all donations matching the query with parameter 
                "SELECT * FROM Donation WHERE Donor_ID = ?",
                donor_id
            )
            print("\n\033[92mDonations linked to this Donor:\033[0m")
            if donations:
                for d in donations:
                    print(
                        f"\033[92mID:\033[0m {d[0]}, "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                        f"\033[92mDate:\033[0m {d[2]}, "
                        f"\033[92mNotes:\033[0m {d[3]}, "
                        f"\033[92mBeneficiary ID:\033[0m {d[7]}"
                    )
            else:
                print("\033[93mNo donations found for this donor.\033[0m")

        elif choice == "2":
            # Search Donations by Event
            print("\n\033[93mTip: Insert an Event ID to search related donations.\033[0m")
            event_id = input("Enter Event ID: ").strip()
            if not event_id.isdigit():
                print("\033[91m🚫 Event ID must be numeric.\033[0m")
                continue

            donations = fetch_all( # Fetch all donations from the database  Execute SQL query to select all donations matching the query with parameter
                "SELECT * FROM Donation WHERE Event_ID = ?",
                event_id
            )
            print("\n\033[92mDonations linked to this Event:\033[0m")
            if donations:
                for d in donations:
                    print(
                        f"\033[92mID:\033[0m {d[0]}, "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                        f"\033[92mDate:\033[0m {d[2]}, "
                        f"\033[92mNotes:\033[0m {d[3]}, "
                        f"\033[92mBeneficiary ID:\033[0m {d[7]}"
                    )
            else:
                print("\033[93mNo donations found for this event.\033[0m")

        elif choice == "3":
            # Search Donations by Business
            print("\n\033[93mTip: Insert a Business ID to search related donations.\033[0m")
            business_id = input("Enter Business ID: ").strip()
            if not business_id.isdigit():
                print("\033[91m🚫 Business ID must be numeric.\033[0m")
                continue

            donations = fetch_all(
                "SELECT * FROM Donation WHERE Business_ID = ?",
                business_id
            )
            print("\n\033[92mDonations linked to this Business:\033[0m")
            if donations:
                for d in donations:
                    print(
                        f"\033[92mID:\033[0m {d[0]}, "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                        f"\033[92mDate:\033[0m {d[2]}, "
                        f"\033[92mNotes:\033[0m {d[3]}, "
                        f"\033[92mBeneficiary ID:\033[0m {d[7]}"
                    )
            else:
                print("\033[93mNo donations found for this business.\033[0m")

        elif choice == "4":
            # Search Donations by Beneficiary
            print("\n\033[93mTip: Insert a Beneficiary ID to search related donations.\033[0m")
            beneficiary_id = input("Enter Beneficiary ID: ").strip()
            if not beneficiary_id.isdigit():
                print("\033[91m🚫 Beneficiary ID must be numeric.\033[0m")
                continue

            donations = fetch_all(
                "SELECT * FROM Donation WHERE Beneficiary_ID = ?",
                beneficiary_id
            )
            print("\n\033[92mDonations linked to this Beneficiary:\033[0m")
            if donations:
                for d in donations:
                    print(
                        f"\033[92mID:\033[0m {d[0]}, "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                        f"\033[92mDate:\033[0m {d[2]}, "
                        f"\033[92mNotes:\033[0m {d[3]}"
                    )
            else:
                print("\033[93mNo donations found for this beneficiary.\033[0m")

        elif choice == "5":
            break

if __name__ == "__main__":
    search_menu()
