# search.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module provides search functionality across the donation system.
It allows users to find records based on relationships between entities:
- Donations by donor, event, business, beneficiary, or volunteer
"""

from start.tables import get_connection

# Fetch query results based on parameter
def fetch_all(query, param):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (param,))
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

# Helper to get Event ID from Volunteer ID
def get_event_id_by_volunteer(volunteer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Event_ID FROM Volunteer WHERE Volunteer_ID = ?", (volunteer_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def search_menu():
    while True:
        # Print menu options with decoration
        print("\n" + "🔎  SEARCH MANAGEMENT MENU  🔍".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  Search Donations by Donor")
        print("2️⃣  Search Donations by Event")
        print("3️⃣  Search Donations by Business")
        print("4️⃣  Search Donations by Beneficiary")
        print("5️⃣  Search Donations by Volunteer")
        print("6️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n🌟 Choose an option (1-6): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5", "6"]:
            print("\033[91m🚫 Invalid option. Please choose a number between 1 and 6.\033[0m")
            continue

        if choice == "1":
            # Search Donations by Donor
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Donor")
                donors = cursor.fetchall()
                conn.close()

                if not donors:
                    print("\033[93mNo donors available.\033[0m")
                    continue

                print("\n\033[92mHere are all Donors:\033[0m")
                for d in donors:
                    print(f"\033[92mDonor ID:\033[0m {d[0]} "
                          f"\033[92mName:\033[0m {d[1]} {d[2]} "
                          f"\033[92mEmail:\033[0m {d[3]} "
                          f"\033[92mPhone:\033[0m {d[4]} "
                          f"\033[92mAddress:\033[0m {d[5]} "
                          f"\033[92mDOB:\033[0m {d[6]}")

                print("\n\033[93mTip: Insert a Donor ID to search donations.\033[0m")
                donor_id = input("Enter Donor ID: ").strip()
                if not donor_id.isdigit():
                    print("\033[91m🚫 Donor ID must be numeric.\033[0m")
                    continue

                query = """
                SELECT Donation.Donation_ID, Donation.Amount, Donation.Date, Donation.Notes,
                       Donor.First_Name, Donor.Last_Name, Beneficiary.Name
                FROM Donation
                JOIN Donor ON Donation.Donor_ID = Donor.Donor_ID
                JOIN Beneficiary ON Donation.Beneficiary_ID = Beneficiary.Beneficiary_ID
                WHERE Donation.Donor_ID = ?
                """

                donations = fetch_all(query, donor_id)

                print("\n\033[92mDonations linked to this Donor:\033[0m")
                if donations:
                    for d in donations:
                        print(
                            f"\033[92mID:\033[0m {d[0]}, "
                            f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                            f"\033[92mDate:\033[0m {d[2]}, "
                            f"\033[92mNotes:\033[0m {d[3]}, "
                            f"\033[92mDonor:\033[0m {d[4]} {d[5]}, "
                            f"\033[92mBeneficiary:\033[0m {d[6]}"
                        )
                else:
                    print("\033[93mNo donations found for this donor.\033[0m")

            except Exception as e:
                print(f"\033[91m🚫 Error searching donations by donor: {e}\033[0m")

        elif choice == "2":
            # Search Donations by Event
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Event")
                events = cursor.fetchall()
                conn.close()

                if not events:
                    print("\033[93mNo events available.\033[0m")
                    continue

                print("\n\033[92mHere are all Events:\033[0m")
                for e in events:
                    print(f"\033[92mEvent ID:\033[0m {e[0]} "
                          f"\033[92mName:\033[0m {e[1]} "
                          f"\033[92mDate:\033[0m {e[2]} "
                          f"\033[92mLocation:\033[0m {e[3]} "
                          f"\033[92mGoal:\033[0m £{e[4]:,.2f} "
                          f"\033[92mDescription:\033[0m {e[5]}")

                print("\n\033[93mTip: Insert an Event ID to search donations.\033[0m")
                event_id = input("Enter Event ID: ").strip()
                if not event_id.isdigit():
                    print("\033[91m🚫 Event ID must be numeric.\033[0m")
                    continue

                query = """
                SELECT Donation.Donation_ID, Donation.Amount, Donation.Date, Donation.Notes,
                       Event.Name, Beneficiary.Name
                FROM Donation
                JOIN Event ON Donation.Event_ID = Event.Event_ID
                JOIN Beneficiary ON Donation.Beneficiary_ID = Beneficiary.Beneficiary_ID
                WHERE Donation.Event_ID = ?
                """

                donations = fetch_all(query, event_id)

                print("\n\033[92mDonations linked to this Event:\033[0m")
                if donations:
                    for d in donations:
                        print(
                            f"\033[92mID:\033[0m {d[0]}, "
                            f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                            f"\033[92mDate:\033[0m {d[2]}, "
                            f"\033[92mNotes:\033[0m {d[3]}, "
                            f"\033[92mEvent:\033[0m {d[4]}, "
                            f"\033[92mBeneficiary:\033[0m {d[5]}"
                        )
                else:
                    print("\033[93mNo donations found for this event.\033[0m")

            except Exception as e:
                print(f"\033[91m🚫 Error searching donations by event: {e}\033[0m")

        elif choice == "3":
            # Search Donations by Business
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Business")
                businesses = cursor.fetchall()
                conn.close()

                if not businesses:
                    print("\033[93mNo businesses available.\033[0m")
                    continue

                print("\n\033[92mHere are all Businesses:\033[0m")
                for b in businesses:
                    print(f"\033[92mBusiness ID:\033[0m {b[0]} "
                          f"\033[92mName:\033[0m {b[1]} "
                          f"\033[92mEmail:\033[0m {b[2]} "
                          f"\033[92mPhone:\033[0m {b[3]} "
                          f"\033[92mAddress:\033[0m {b[4]} "
                          f"\033[92mRegistration Date:\033[0m {b[5]}")

                print("\n\033[93mTip: Insert a Business ID to search donations.\033[0m")
                business_id = input("Enter Business ID: ").strip()
                if not business_id.isdigit():
                    print("\033[91m🚫 Business ID must be numeric.\033[0m")
                    continue

                query = """
                SELECT Donation.Donation_ID, Donation.Amount, Donation.Date, Donation.Notes,
                       Business.Name, Beneficiary.Name
                FROM Donation
                JOIN Business ON Donation.Business_ID = Business.Business_ID
                JOIN Beneficiary ON Donation.Beneficiary_ID = Beneficiary.Beneficiary_ID
                WHERE Donation.Business_ID = ?
                """

                donations = fetch_all(query, business_id)

                print("\n\033[92mDonations linked to this Business:\033[0m")
                if donations:
                    for d in donations:
                        print(
                            f"\033[92mID:\033[0m {d[0]}, "
                            f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                            f"\033[92mDate:\033[0m {d[2]}, "
                            f"\033[92mNotes:\033[0m {d[3]}, "
                            f"\033[92mBusiness:\033[0m {d[4]}, "
                            f"\033[92mBeneficiary:\033[0m {d[5]}"
                        )
                else:
                    print("\033[93mNo donations found for this business.\033[0m")

            except Exception as e:
                print(f"\033[91m🚫 Error searching donations by business: {e}\033[0m")

        elif choice == "4":
            # Search Donations by Beneficiary
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Beneficiary")
                beneficiaries = cursor.fetchall()
                conn.close()

                if not beneficiaries:
                    print("\033[93mNo beneficiaries available.\033[0m")
                    continue

                print("\n\033[92mHere are all Beneficiaries:\033[0m")
                for b in beneficiaries:
                    print(f"\033[92mBeneficiary ID:\033[0m {b[0]} "
                          f"\033[92mName:\033[0m {b[1]} "
                          f"\033[92mType:\033[0m {b[2]} "
                          f"\033[92mAddress:\033[0m {b[3]} "
                          f"\033[92mSupport Duration:\033[0m {b[4]} "
                          f"\033[92mFunding Priority:\033[0m {b[5]}")

                print("\n\033[93mTip: Insert a Beneficiary ID to search donations.\033[0m")
                beneficiary_id = input("Enter Beneficiary ID: ").strip()
                if not beneficiary_id.isdigit():
                    print("\033[91m🚫 Beneficiary ID must be numeric.\033[0m")
                    continue

                query = """
                SELECT Donation.Donation_ID, Donation.Amount, Donation.Date, Donation.Notes,
                       Beneficiary.Name
                FROM Donation
                JOIN Beneficiary ON Donation.Beneficiary_ID = Beneficiary.Beneficiary_ID
                WHERE Donation.Beneficiary_ID = ?
                """

                donations = fetch_all(query, beneficiary_id)

                print("\n\033[92mDonations linked to this Beneficiary:\033[0m")
                if donations:
                    for d in donations:
                        print(
                            f"\033[92mID:\033[0m {d[0]}, "
                            f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                            f"\033[92mDate:\033[0m {d[2]}, "
                            f"\033[92mNotes:\033[0m {d[3]}, "
                            f"\033[92mBeneficiary:\033[0m {d[4]}"
                        )
                else:
                    print("\033[93mNo donations found for this beneficiary.\033[0m")

            except Exception as e:
                print(f"\033[91m🚫 Error searching donations by beneficiary: {e}\033[0m")

        elif choice == "5":
            # Search Donations by Volunteer
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT Volunteer.Volunteer_ID, Volunteer.First_Name, Volunteer.Last_Name,
                           Volunteer.Address, Volunteer.Date_of_Birth, Volunteer.Contact_Number,
                           Event.Event_ID, Event.Name
                    FROM Volunteer
                    JOIN Event ON Volunteer.Event_ID = Event.Event_ID
                """)
                volunteers = cursor.fetchall()
                conn.close()

                if not volunteers:
                    print("\033[93mNo volunteers available.\033[0m")
                    continue

                print("\n\033[92mHere are all Volunteers:\033[0m")
                for v in volunteers:
                    print(f"\033[92mVolunteer ID:\033[0m {v[0]} "
                          f"\033[92mName:\033[0m {v[1]} {v[2]} "
                          f"\033[92mAddress:\033[0m {v[3]} "
                          f"\033[92mDOB:\033[0m {v[4]} "
                          f"\033[92mContact:\033[0m {v[5]} "
                          f"\033[92mEvent ID:\033[0m {v[6]} "
                          f"\033[92mEvent Name:\033[0m {v[7]}")

                print("\n\033[93mTip: Insert a Volunteer ID to search donations based on their event.\033[0m")
                volunteer_id = input("Enter Volunteer ID: ").strip()
                if not volunteer_id.isdigit():
                    print("\033[91m🚫 Volunteer ID must be numeric.\033[0m")
                    continue

                event_id = get_event_id_by_volunteer(volunteer_id)
                if not event_id:
                    print("\033[93mNo event found linked to this Volunteer.\033[0m")
                    continue

                query = """
                SELECT Donation.Donation_ID, Donation.Amount, Donation.Date, Donation.Notes,
                       Event.Name, Beneficiary.Name
                FROM Donation
                JOIN Event ON Donation.Event_ID = Event.Event_ID
                JOIN Beneficiary ON Donation.Beneficiary_ID = Beneficiary.Beneficiary_ID
                WHERE Donation.Event_ID = ?
                """

                donations = fetch_all(query, event_id)

                print("\n\033[92mDonations linked to the Event where this Volunteer worked:\033[0m")
                if donations:
                    for d in donations:
                        print(
                            f"\033[92mID:\033[0m {d[0]}, "
                            f"\033[92mAmount:\033[0m £{d[1]:,.2f}, "
                            f"\033[92mDate:\033[0m {d[2]}, "
                            f"\033[92mNotes:\033[0m {d[3]}, "
                            f"\033[92mEvent:\033[0m {d[4]}, "
                            f"\033[92mBeneficiary:\033[0m {d[5]}"
                        )
                else:
                    print("\033[93mNo donations found linked to this volunteer's event.\033[0m")

            except Exception as e:
                print(f"\033[91m🚫 Error searching donations by volunteer: {e}\033[0m")


if __name__ == "__main__":
    search_menu()
