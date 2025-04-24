# volunteer.py
#In this page i used the same crud concept explained for beneficiary.py view, create,update and delete with minor changes
"""
This module handles all volunteer-related operations in the donation system.
It provides a menu interface for managing volunteer records including:
- Viewing all volunteers
- Adding new volunteers
- Updating existing volunteers
- Deleting volunteers (with donation checks)
"""

import re  # For date validation
from start.crud import view_all, add_entry, update_entry, delete_entry
from start.tables import get_connection

def volunteer_menu():
    while True:
        # Display menu options with green header
        print("\n\033[92m--- Volunteer Management ---\033[0m", flush=True)
        print("1. View All Volunteers")
        print("2. Add Volunteer")
        print("3. Update Volunteer")
        print("4. Delete Volunteer")
        print("5. Back to Main Menu")
        
        choice = input("\033[92mChoose an option (1-5): \033[0m").strip()

        # Validate menu choice
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91mInvalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        # Option 1: View all volunteers
        if choice == "1":
            try:
                print("\n\033[92mAll Volunteers:\033[0m")
                volunteers = view_all("Volunteer")
                if not volunteers:
                    print("\033[93mNo volunteers found in database.\033[0m")
                else:
                    for v in volunteers:
                        print(
                            f"\033[92mVolunteer ID:\033[0m {v[0]} "
                            f"\033[92mName:\033[0m {v[1]} {v[2]} "
                            f"\033[92mEmail:\033[0m {v[3]} "
                            f"\033[92mPhone:\033[0m {v[4]} "
                            f"\033[92mEvent ID:\033[0m {v[7]}"
                        )
            except Exception as e:
                print(f"\033[91mError viewing volunteers: {str(e)}\033[0m")

        # Option 2: Add new volunteer
        elif choice == "2":
            try:
                fname = input("First Name: ").strip()
                if not fname.replace(" ", "").isalpha():
                    print("\033[91mFirst name must contain only letters.\033[0m")
                    continue
                fname = fname.capitalize()

                lname = input("Last Name: ").strip()
                if not lname.replace(" ", "").isalpha():
                    print("\033[91mLast name must contain only letters.\033[0m")
                    continue
                lname = lname.capitalize()

                email = input("Email: ").strip()
                if "@" not in email or "." not in email:
                    print("\033[91mPlease enter a valid email address.\033[0m")
                    continue

                phone = input("Phone Number: ").strip()
                if not phone.isdigit():
                    print("\033[91mPhone number must contain only digits.\033[0m")
                    continue

                address = input("Address: ").strip()

                dob = input("Date of Birth (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                    print("\033[91mDOB must be in format YYYY-MM-DD using only numbers.\033[0m")
                    continue

                event_id = input("Event ID: ").strip()
                if not event_id.isdigit():
                    print("\033[91mEvent ID must be a number.\033[0m")
                    continue

                add_entry(
                    "INSERT INTO Volunteer VALUES (NULL,?,?,?,?,?,?,?)",
                    (fname, lname, email, phone, address, dob, event_id)
                )
                print("\033[92mVolunteer added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError adding volunteer: {str(e)}\033[0m")

        elif choice == "3":
            try:
                vid = input("Enter Volunteer ID to update: ").strip()
                if not vid.isdigit():
                    print("\033[91mVolunteer ID must be a number.\033[0m")
                    continue

                fname = input("First Name: ").strip()
                if not fname.replace(" ", "").isalpha():
                    print("\033[91mFirst name must contain only letters.\033[0m")
                    continue
                fname = fname.capitalize()

                lname = input("Last Name: ").strip()
                if not lname.replace(" ", "").isalpha():
                    print("\033[91mLast name must contain only letters.\033[0m")
                    continue
                lname = lname.capitalize()

                email = input("Email: ").strip()
                if "@" not in email or "." not in email:
                    print("\033[91mPlease enter a valid email address.\033[0m")
                    continue

                phone = input("Phone Number: ").strip()
                if not phone.isdigit():
                    print("\033[91mPhone number must contain only digits.\033[0m")
                    continue

                address = input("Address: ").strip()

                dob = input("New Date of Birth (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                    print("\033[91mDOB must be in format YYYY-MM-DD using only numbers.\033[0m")
                    continue

                event_id = input("Event ID: ").strip()
                if not event_id.isdigit():
                    print("\033[91mEvent ID must be a number.\033[0m")
                    continue

                update_entry(
                    "UPDATE Volunteer SET First_Name=?, Last_Name=?, Email=?, Phone_Number=?, Address=?, Date_of_Birth=?, Event_ID=? WHERE Volunteer_ID=?",
                    (fname, lname, email, phone, address, dob, event_id, vid)
                )
                print("\033[92mVolunteer updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError updating volunteer: {str(e)}\033[0m")

        # Option 4: Delete volunteer
        elif choice == "4":
            try:
                vid = input("Enter Volunteer ID to delete: ").strip()
                if not vid.isdigit():
                    print("\033[91mVolunteer ID must be a number.\033[0m")
                    continue

                delete_entry("DELETE FROM Volunteer WHERE Volunteer_ID=?", vid)
                print("\033[92mVolunteer and all related donations deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError deleting volunteer: {str(e)}\033[0m")

        # Option 5: Exit
        elif choice == "5":
            break

if __name__ == "__main__":
    volunteer_menu()
