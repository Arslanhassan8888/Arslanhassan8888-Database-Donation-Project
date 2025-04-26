# donor.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# In this page i used the same crud concept explained for beneficiary.py: view, create, update and delete with minor changes
"""
This module handles all donor-related operations in the donation system.
It provides a menu interface for managing donor records including:
- Viewing all donors
- Adding new donors
- Updating existing donors
- Deleting donors (with donation checks)
"""

import re  # Regular expressions for date and DOB validation
from start.crud import view_all, add_entry, update_entry, delete_entry, has_linked_donations
def donor_menu():

    while True:
        # Print menu options with decoration
        print("\n" + "🎯  DONOR MANAGEMENT MENU  🎯".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  View All Donors")
        print("2️⃣  Add Donor")
        print("3️⃣  Update Donor")
        print("4️⃣  Delete Donor")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n🌟 Choose an option (1-5): ").strip()

        # Validate menu choice
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91m🚫 Invalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        if choice == "1":
            try:
                print("\n\033[92mAll Donors:\033[0m")
                donors = view_all("Donor")
                if not donors:
                    print("\033[93mNo donors found in database.\033[0m")
                else:
                    for donor in donors:
                        print(
                            f"\033[92mID:\033[0m {donor[0]} "
                            f"\033[92mFirst Name:\033[0m {donor[1]} "
                            f"\033[92mLast Name:\033[0m {donor[2]} "
                            f"\033[92mEmail:\033[0m {donor[3]} "
                            f"\033[92mPhone:\033[0m {donor[4]} "
                            f"\033[92mAddress:\033[0m {donor[5]} "
                            f"\033[92mDOB:\033[0m {donor[6]}"
                        )
            except Exception as e:
                print(f"\033[91m🚫 Error viewing donors: {e}\033[0m")

        elif choice == "2":
            try:
                print("\n\033[93mTip: First Name and Last Name must include only letters.\033[0m\n")
                fname = input("First Name: ").strip()
                if not fname.replace(" ", "").isalpha():
                    print("\033[91m🚫 First name must contain only letters.\033[0m")
                    continue
                fname = fname.capitalize() # Capitalize first letter

                lname = input("Last Name: ").strip()
                if not lname.replace(" ", "").isalpha():
                    print("\033[91m🚫 Last name must contain only letters.\033[0m")
                    continue
                lname = lname.capitalize()

                print("\033[93mTip: Use a valid email format, e.g., example@email.com\033[0m")
                email = input("Email: ").strip()
                if "@" not in email or "." not in email:
                    print("\033[91m🚫 Email must contain both '@' and '.'\033[0m")
                    continue

                print("\033[93mTip: Use only numbers for phone, e.g., 07123456789.\033[0m")
                phone = input("Phone Number (digits only): ").strip()
                if not phone.isdigit():
                    print("\033[91m🚫 Phone number must contain only digits.\033[0m")
                    continue

                print("\033[93mTip: Enter full address including street and number.\033[0m")
                address = input("Address: ").strip()

                print("\033[93mTip: Use the format YYYY-MM-DD for date of birth.\033[0m")
                dob = input("Date of Birth (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                    print("\033[91m🚫 DOB must be in format YYYY-MM-DD.\033[0m")
                    continue

                add_entry(
                    "INSERT INTO Donor VALUES (NULL,?,?,?,?,?,?)",
                    (fname, lname, email, phone, address, dob)
                )
                print("\033[92m🎉 Donor added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error adding donor: {e}\033[0m")

        elif choice == "3":
            print("\n\033[92mList of All Donors:\033[0m")
            donors = view_all("Donor")
            for donor in donors:
                print(
                    f"\033[92mID:\033[0m {donor[0]} "
                    f"\033[92mFirst Name:\033[0m {donor[1]} "
                    f"\033[92mLast Name:\033[0m {donor[2]} "
                    f"\033[92mEmail:\033[0m {donor[3]} "
                    f"\033[92mPhone:\033[0m {donor[4]} "
                    f"\033[92mAddress:\033[0m {donor[5]} "
                    f"\033[92mDOB:\033[0m {donor[6]}"
                )
            try:
                print("\n\033[93mTip: Enter the ID of the donor you want to update.\033[0m")
                donor_id = input("Enter Donor ID to update: ").strip()
                if not donor_id.isdigit():
                    print("\033[91m🚫 Donor ID must be numeric.\033[0m")
                    continue

                fname = input("New First Name: ").strip()
                if not fname.replace(" ", "").isalpha():
                    print("\033[91m🚫 First name must contain only letters.\033[0m")
                    continue
                fname = fname.capitalize()

                lname = input("New Last Name: ").strip()
                if not lname.replace(" ", "").isalpha():
                    print("\033[91m🚫 Last name must contain only letters.\033[0m")
                    continue
                lname = lname.capitalize()

                email = input("New Email: ").strip()
                if "@" not in email or "." not in email:
                    print("\033[91m🚫 Email must contain both '@' and '.'\033[0m")
                    continue

                phone = input("New Phone Number (digits only): ").strip()
                if not phone.isdigit():
                    print("\033[91m🚫 Phone number must contain only digits.\033[0m")
                    continue

                address = input("New Address: ").strip()

                dob = input("New Date of Birth (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                    print("\033[91m🚫 DOB must be in format YYYY-MM-DD.\033[0m")
                    continue

                update_entry(
                    "UPDATE Donor SET First_Name=?, Last_Name=?, Email=?, Phone_Number=?, Address=?, Date_of_Birth=? WHERE Donor_ID=?",
                    (fname, lname, email, phone, address, dob, donor_id)
                )
                print("\033[92m🎉 Donor updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error updating donor: {e}\033[0m")

        elif choice == "4":
            print("\n\033[92mList of All Donors:\033[0m")
            donors = view_all("Donor")
            for donor in donors:
                print(
                    f"\033[92mID:\033[0m {donor[0]} "
                    f"\033[92mFirst Name:\033[0m {donor[1]} "
                    f"\033[92mLast Name:\033[0m {donor[2]} "
                    f"\033[92mEmail:\033[0m {donor[3]} "
                    f"\033[92mPhone:\033[0m {donor[4]} "
                    f"\033[92mAddress:\033[0m {donor[5]} "
                    f"\033[92mDOB:\033[0m {donor[6]}"
                )
            try:
                print("\n\033[93mTip: Enter the ID of the donor you want to delete.\033[0m")
                donor_id = input("Enter Donor ID to delete: ").strip()
                if not donor_id.isdigit():
                    print("\033[91m🚫 Donor ID must be numeric.\033[0m")
                    continue

                if has_linked_donations("Donor_ID", donor_id):
                    print("\033[91m🚫 Cannot delete Donor linked to existing Donations.\033[0m")
                    continue

                delete_entry("DELETE FROM Donor WHERE Donor_ID=?", donor_id)
                print("\033[92m🎉 Donor deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error deleting donor: {e}\033[0m")

        elif choice == "5":
            break

if __name__ == "__main__":
    donor_menu()
