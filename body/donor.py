# donor.py
import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module handles all donor-related operations in the donation system.
It provides a menu interface for managing donor records including:
- Viewing all donors
- Adding new donors
- Updating existing donors
- Deleting donors (with donation checks)
"""

from start.crud import view_all, add_entry, update_entry, delete_entry, linked_donations

def display_donors(donors):
    """Display all donor records in a consistent format"""
    if not donors:
        print("\033[93mNo donors found in database.\033[0m")
        return False
    for i in donors:
        print(
            f"\033[92mID:\033[0m {i[0]} "
            f"\033[92mName:\033[0m {i[1]} {i[2]} "
            f"\033[92mEmail:\033[0m {i[3]} "
            f"\033[92mPhone:\033[0m {i[4]} "
            f"\033[92mAddress:\033[0m {i[5]} "
            f"\033[92mDOB:\033[0m {i[6]}"
        )
    return True

def donor_input(action):
    """Collect and validate donor information from user"""
    print("\n\033[93mTip: Names should contain only letters.\033[0m")
    
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

    print("\033[93mTip: Use a valid email format (e.g., name@example.com).\033[0m")
    email = input(f"{action} Email: ").strip()
    if "@" not in email or "." not in email:
        print("\033[91m🚫 Please enter a valid email address.\033[0m")
        return None

    print("\033[93mTip: Phone number must be digits only.\033[0m")
    phone = input(f"{action} Phone Number: ").strip()
    if not phone.isdigit():
        print("\033[91m🚫 Phone number must contain only digits.\033[0m")
        return None

    address = input(f"{action} Address: ").strip()

    print("\033[93mTip: Use format YYYY-MM-DD for date of birth.\033[0m")
    dob = input(f"{action} Date of Birth (YYYY-MM-DD): ").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
        print("\033[91m🚫 Date must be in format YYYY-MM-DD.\033[0m")
        return None

    return (first_name, last_name, email, phone, address, dob)

def donor_menu():
    """
    Main donor management interface
    Handles all CRUD operations for donors through a menu system
    """
    while True:
        # Display menu options
        print("\n" + "🎯  DONOR MANAGEMENT MENU  🎯".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  View All Donors")
        print("2️⃣  Add Donor")
        print("3️⃣  Update Donor")
        print("4️⃣  Delete Donor")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n Choose an option (1-5): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91m🚫 Invalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        # View all donors
        if choice == "1":
            try:
                print("\n\033[92mAll Donors:\033[0m")
                donors = view_all("Donor")
                display_donors(donors)
            except Exception as e:
                print(f"\033[91m🚫 Error viewing donors: {str(e)}\033[0m")

        # Add new donor
        elif choice == "2":
            try:
                data = donor_input("Add")
                if data:
                    add_entry(
                        "INSERT INTO Donor VALUES (NULL,?,?,?,?,?,?)",
                        data
                    )
                    print("\033[92m🎉 Donor added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error adding donor: {str(e)}\033[0m")

        # Update existing donor
        elif choice == "3":
            try:
                print("\n\033[92mList of All Donors:\033[0m")
                donors = view_all("Donor")
                if not display_donors(donors):
                    continue

                donor_id = input("\nEnter Donor ID to update: ").strip()
                if not donor_id.isdigit():
                    print("\033[91m🚫 Donor ID must be numeric.\033[0m")
                    continue

                data = donor_input("New")
                if data:
                    update_entry(
                        "UPDATE Donor SET First_Name=?, Last_Name=?, Email=?, Phone_Number=?, Address=?, Date_of_Birth=? WHERE Donor_ID=?",
                        (*data, donor_id)
                    )
                    print("\033[92m🎉 Donor updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error updating donor: {str(e)}\033[0m")

        # Delete donor
        elif choice == "4":
            try:
                print("\n\033[92mList of All Donors:\033[0m")
                donors = view_all("Donor")
                if not display_donors(donors):
                    continue

                donor_id = input("\nEnter Donor ID to delete: ").strip()
                if not donor_id.isdigit():
                    print("\033[91m🚫 Donor ID must be numeric.\033[0m")
                    continue

                if linked_donations("Donor_ID", donor_id):
                    print("\033[91m🚫 Cannot delete Donor linked to existing Donations.\033[0m")
                    continue

                delete_entry("DELETE FROM Donor WHERE Donor_ID=?", donor_id)
                print("\033[92m🎉 Donor deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error deleting donor: {str(e)}\033[0m")

        # Return to main menu
        elif choice == "5":
            break

if __name__ == "__main__":
    donor_menu()