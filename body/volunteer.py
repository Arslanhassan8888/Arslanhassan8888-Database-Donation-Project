# volunteer.py
import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module handles all volunteer-related operations in the donation system.
It provides a menu interface for managing volunteer records linked to events, including:
- Viewing all volunteers
- Adding new volunteers
- Updating existing volunteers
- Deleting volunteers
"""

from start.crud import view_all, add_entry, update_entry, delete_entry

def display_volunteers(volunteers):
    """Display all volunteer records in a consistent format"""
    if not volunteers:
        print("\033[93mNo volunteers found in database.\033[0m")
        return False
    for v in volunteers:
        print(
            f"\033[92mID:\033[0m {v[0]} "
            f"\033[92mEvent ID:\033[0m {v[1]} "
            f"\033[92mName:\033[0m {v[2]} {v[3]} "
            f"\033[92mAddress:\033[0m {v[4]} "
            f"\033[92mDOB:\033[0m {v[5]} "
            f"\033[92mContact:\033[0m {v[6]}"
        )
    return True

def volunteer_input(action):
    """Collect and validate volunteer information from user"""
    print("\n\033[93mTip: Make sure Event ID exists before adding volunteer.\033[0m")
    event_id = input(f"{action} Event ID: ").strip()
    if not event_id.isdigit():
        print("\033[91m🚫 Event ID must be numeric.\033[0m")
        return None

    print("\033[93mTip: Names should contain only letters.\033[0m")
    first_name = input(f"{action} First Name: ").strip()
    if not first_name.replace(" ", "").isalpha():
        print("\033[91m🚫 First name must contain only letters.\033[0m")
        return None
    first_name = first_name.capitalize()

    last_name = input(f"{action} Last Name: ").strip()
    if not last_name.replace(" ", "").isalpha():
        print("\033[91m🚫 Last name must contain only letters.\033[0m")
        return None
    last_name = last_name.capitalize()

    address = input(f"{action} Address: ").strip()

    print("\033[93mTip: Use format YYYY-MM-DD for date of birth.\033[0m")
    dob = input(f"{action} Date of Birth (YYYY-MM-DD): ").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
        print("\033[91m🚫 Date must be in format YYYY-MM-DD.\033[0m")
        return None

    print("\033[93mTip: Contact number must be digits only.\033[0m")
    contact = input(f"{action} Contact Number: ").strip()
    if not contact.isdigit():
        print("\033[91m🚫 Contact number must contain only digits.\033[0m")
        return None

    return (event_id, first_name, last_name, address, dob, contact)

def volunteer_menu():
    """
    Main volunteer management interface
    Handles all CRUD operations for volunteers through a menu system
    """
    while True:
        # Display menu options
        print("\n" + "🎯  VOLUNTEER MANAGEMENT MENU  🎯".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  View All Volunteers")
        print("2️⃣  Add Volunteer")
        print("3️⃣  Update Volunteer")
        print("4️⃣  Delete Volunteer")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n Choose an option (1-5): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91m🚫 Invalid choice. Please choose between 1-5.\033[0m")
            continue

        if choice == "1":
            try:
                print("\n\033[92mAll Volunteers:\033[0m")
                volunteers = view_all("Volunteer")
                display_volunteers(volunteers)
            except Exception as e:
                print(f"\033[91m🚫 Error viewing volunteers: {str(e)}\033[0m")

        elif choice == "2":
            try:
                data = volunteer_input("Add")
                if data:
                    add_entry(
                        "INSERT INTO Volunteer (Event_ID, First_Name, Last_Name, Address, Date_of_Birth, Contact_Number) VALUES (?,?,?,?,?,?)",
                        data
                    )
                    print("\033[92m🎉 Volunteer added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error adding volunteer: {str(e)}\033[0m")

        elif choice == "3":
            try:
                print("\n\033[92mList of All Volunteers:\033[0m")
                volunteers = view_all("Volunteer")
                if not display_volunteers(volunteers):
                    continue

                volunteer_id = input("\nEnter Volunteer ID to update: ").strip()
                if not volunteer_id.isdigit():
                    print("\033[91m🚫 Volunteer ID must be numeric.\033[0m")
                    continue

                data = volunteer_input("New")
                if data:
                    update_entry(
                        "UPDATE Volunteer SET Event_ID=?, First_Name=?, Last_Name=?, Address=?, Date_of_Birth=?, Contact_Number=? WHERE Volunteer_ID=?",
                        (*data, volunteer_id)
                    )
                    print("\033[92m🎉 Volunteer updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error updating volunteer: {str(e)}\033[0m")

        elif choice == "4":
            try:
                print("\n\033[92mList of All Volunteers:\033[0m")
                volunteers = view_all("Volunteer")
                if not display_volunteers(volunteers):
                    continue

                volunteer_id = input("\nEnter Volunteer ID to delete: ").strip()
                if not volunteer_id.isdigit():
                    print("\033[91m🚫 Volunteer ID must be numeric.\033[0m")
                    continue

                delete_entry("DELETE FROM Volunteer WHERE Volunteer_ID=?", volunteer_id)
                print("\033[92m🎉 Volunteer deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error deleting volunteer: {str(e)}\033[0m")

        elif choice == "5":
            break

if __name__ == "__main__":
    volunteer_menu()
