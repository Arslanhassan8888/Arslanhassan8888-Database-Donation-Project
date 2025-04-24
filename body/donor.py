# donor.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#In this page i used the same crud concept explained for beneficiary.py view, create,update and delete with minor changes
"""
This module handles all donor-related operations in the donation system.
It provides a menu interface for managing donor records including:
- Viewing all donors
- Adding new donors
- Updating existing donors
- Deleting donors (with donation checks)
"""
import re    # Regular expressions for date and Dob validation. it's Python’s built-in re module.
from start.crud import view_all, add_entry, update_entry, delete_entry


"""
    Displays and manages the donor management menu.
    Provides a continuous interface for donor operations until user exits.
    Handles all CRUD operations for donor records.
"""
def donor_menu():
    while True:
        print("\n\033[92m--- Donor Management ---\033[0m", flush=True)
        print("1. View All Donors")
        print("2. Add Donor")
        print("3. Update Donor")
        print("4. Delete Donor")
        print("5. Back to Main Menu")

        choice = input("\033[92mChoose an option (1-5): \033[0m").strip()
        # Validate menu choice is a number 1-5
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91mInvalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        if choice == "1":
            try:
                print("\n\033[92mAll Donors:\033[0m")
                for donor in view_all("Donor"):
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
                print(f"\033[91mAn error occurred while viewing donors: {e}\033[0m")

        elif choice == "2":
            try:
                print("\033[93mTip: First Name and Last Name must include only letters.\033[0m")
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

                print("\033[93mTip: Use a valid email format, e.g., example@email.com\033[0m")
                email = input("Email: ").strip()
                if "@" not in email or "." not in email:
                    print("\033[91mEmail must contain both '@' and '.'\033[0m")
                    continue

                print("\033[93mTip: Use only numbers, e.g., 07123456789.\033[0m")
                phone = input("Phone Number (digits only): ").strip()
                if not phone.isdigit():
                    print("\033[91mPhone number must contain only digits.\033[0m")
                    continue

                print("\033[93mTip: Enter full address including street and number (e.g., 123 King Street).\033[0m")
                address = input("Address: ").strip()

                print("\033[93mTip: Use the format YYYY-MM-DD for date of birth (e.g., 1980-06-15).\033[0m")
                dob = input("Date of Birth (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                    print("\033[91mDOB must be in format YYYY-MM-DD using only numbers.\033[0m")
                    continue

                add_entry(
                    "INSERT INTO Donor VALUES (NULL,?,?,?,?,?,?)",
                    (fname, lname, email, phone, address, dob)
                )
                print("\033[92mDonor added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError adding donor: {e}\033[0m")

        elif choice == "3":
            print("\n\033[92mList of All Donors:\033[0m")
            for donor in view_all("Donor"):
                print(
                    f"\033[92mID:\033[0m {donor[0]} "
                    f"\033[92mFirst Name:\033[0m {donor[1]} "
                    f"\033[92mLast Name:\033[0m {donor[2]}"
                    )
            try:
                print("\033[93mTip: Please enter the ID number of the donor you wish to update.\033[0m")
                donor_id = input("Enter Donor ID to update: ").strip()
                if not donor_id.isdigit():
                    print("\033[91mDonor ID must be numeric.\033[0m")
                    continue
                print("\033[93mTip: First name and Last Name must only include letters.\033[0m")
                fname = input("New First Name: ").strip()
                if not fname.replace(" ", "").isalpha():
                    print("\033[91mFirst name must contain only letters.\033[0m")
                    continue
                fname = fname.capitalize()

                lname = input("New Last Name: ").strip()
                if not lname.replace(" ", "").isalpha():
                    print("\033[91mLast name must contain only letters.\033[0m")
                    continue
                lname = lname.capitalize()

                print("\033[93mTip: Use a valid email format, e.g., example@email.com\033[0m")
                email = input("New Email: ").strip()
                if "@" not in email or "." not in email:
                    print("\033[91mEmail must contain both '@' and '.'\033[0m")
                    continue
                
                print("\033[93mTip: Use only numbers, e.g., 07123456789.\033[0m")
                phone = input("New Phone Number: ").strip()
                if not phone.isdigit():
                    print("\033[91mPhone number must contain only digits.\033[0m")
                    continue

                print("\033[93mTip: Update the full address if needed.\033[0m")
                address = input("New Address: ").strip()

                print("\033[93mTip: Use date format YYYY-MM-DD for date of birth.\033[0m")
                dob = input("New Date of Birth (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                    print("\033[91mDOB must be in format YYYY-MM-DD using only numbers.\033[0m")
                    continue

                update_entry(
                    "UPDATE Donor SET First_Name=?, Last_Name=?, Email=?, Phone_Number=?, Address=?, Date_of_Birth=? WHERE Donor_ID=?",
                    (fname, lname, email, phone, address, dob, donor_id)
                )
                print("\033[92mDonor updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError updating donor: {e}\033[0m")

        elif choice == "4":
            try:
                print("\033[93mTip: Please enter the ID number of the donor you wish to update.\033[0m")
                print("\033[93mTip: Deleting a donor will also delete all their donations.\033[0m")
                donor_id = input("Enter Donor ID to delete: ").strip()
                if not donor_id.isdigit():
                    print("\033[91mDonor ID must be numeric.\033[0m")
                    continue

                delete_entry("DELETE FROM Donor WHERE Donor_ID=?", donor_id)
                print("\033[92mDonor and all related donations deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError deleting donor: {e}\033[0m")

        elif choice == "5":
            break

if __name__ == "__main__":
    donor_menu()
