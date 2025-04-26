# business.py 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module handles all business-related operations in the donation system.
It provides a menu interface for managing business records including:
- Viewing all businesses
- Adding new businesses
- Updating existing businesses
- Deleting businesses (with donation checks)
"""

import re  # For date validation
from start.crud import view_all, add_entry, update_entry, delete_entry, has_linked_donations

def business_menu():
    """
    Displays and manages the business management menu.
    Provides continuous interface for business operations until user exits.
    Handles all CRUD operations for business records with proper validation.

    """

    while True:
        # Print menu options with decoration
        print("\n" + "🎯  BUSINESS MANAGEMENT MENU  🎯".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  View All Businesses")
        print("2️⃣  Add Business")
        print("3️⃣  Update Business")
        print("4️⃣  Delete Business")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n🌟 Choose an option (1-5): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91m🚫 Invalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        # Option 1: View all businesses
        if choice == "1":
            try:
                print("\n\033[92mAll Businesses:\033[0m")
                businesses = view_all("Business")
                if not businesses:
                    print("\033[93mNo businesses found in database.\033[0m")
                else:
                    for b in businesses:
                        print(
                            f"\033[92mID:\033[0m {b[0]} "
                            f"\033[92mBusiness Name:\033[0m {b[1]} "
                            f"\033[92mEmail:\033[0m {b[2]} "
                            f"\033[92mPhone:\033[0m {b[3]} "
                            f"\033[92mAddress:\033[0m {b[4]} "
                            f"\033[92mDate of Registration:\033[0m {b[5]}"
                        )
            except Exception as e:
                print(f"\033[91m🚫 Error viewing businesses: {str(e)}\033[0m")

        # Option 2: Add new business
        elif choice == "2":
            try:
                print("\n\033[93mTip: Business Name should only contain letters.\033[0m\n")
                name = input("Business Name: ").strip()
                if not name.replace(" ", "").isalpha():
                    print("\033[91m🚫 Business name must contain only letters.\033[0m")
                    continue
                name = name.capitalize()

                print("\033[93mTip: Use a valid email address (e.g., name@business.com).\033[0m")
                email = input("Email: ").strip()
                if "@" not in email or "." not in email:  # Check if email contains '@' and '.' to validate
                    print("\033[91m🚫 Please enter a valid email address.\033[0m")
                    continue

                print("\033[93mTip: Phone number must be digits only.\033[0m")
                phone = input("Phone Number (digits only): ").strip() # Check if it contains only digits
                if not phone.isdigit():
                    print("\033[91m🚫 Phone number must contain only digits.\033[0m")
                    continue

                print("\033[93mTip: Address cannot be empty.\033[0m")
                address = input("Address: ").strip()

                print("\033[93mTip: Use format YYYY-MM-DD for Date of Registration.\033[0m")
                registration_date = input("Date of Registration (YYYY-MM-DD): ").strip() # Validate date format  Check if date is in YYYY-MM-DD format using regex
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", registration_date): 
                    print("\033[91m🚫 Date must be in format YYYY-MM-DD.\033[0m")
                    continue

                add_entry(
                    "INSERT INTO Business VALUES (NULL,?,?,?,?,?)",  # Insert new business into the database
                    (name, email, phone, address, registration_date)
                )
                print("\033[92m🎉 Business added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error adding business: {str(e)}\033[0m")

        # Option 3: Update business
        elif choice == "3":
            try:
                print("\n\033[92mList of All Businesses:\033[0m")
                businesses = view_all("Business")
                if not businesses:
                    print("\033[93mNo businesses found to update.\033[0m")
                    continue
                for b in businesses:
                    print(
                        f"\033[92mID:\033[0m {b[0]} "
                        f"\033[92mBusiness Name:\033[0m {b[1]} "
                        f"\033[92mEmail:\033[0m {b[2]} "
                        f"\033[92mPhone:\033[0m {b[3]} "
                        f"\033[92mAddress:\033[0m {b[4]} "
                        f"\033[92mDate of Registration:\033[0m {b[5]}"
                    )

                print("\033[93mTip: Please enter the ID number of the business you wish to update.\033[0m")
                business_id = input("Enter Business ID to update: ").strip()
                if not business_id.isdigit():
                    print("\033[91m🚫 Business ID must be numeric.\033[0m")
                    continue

                name = input("New Business Name: ").strip()
                if not name.replace(" ", "").isalpha():
                    print("\033[91m🚫 Business name must contain only letters.\033[0m")
                    continue
                name = name.capitalize()

                email = input("New Email: ").strip()
                if "@" not in email or "." not in email:
                    print("\033[91m🚫 Please enter a valid email address.\033[0m")
                    continue

                phone = input("New Phone Number (digits only): ").strip()
                if not phone.isdigit():
                    print("\033[91m🚫 Phone number must contain only digits.\033[0m")
                    continue

                address = input("New Address: ").strip()

                registration_date = input("New Date of Registration (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", registration_date):
                    print("\033[91m🚫 Date must be in format YYYY-MM-DD.\033[0m")
                    continue

                update_entry(
                    "UPDATE Business SET Name=?, Email=?, Phone_Number=?, Address=?, Registration_Date=? WHERE Business_ID=?",
                    (name, email, phone, address, registration_date, business_id)
                )
                print("\033[92m🎉 Business updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error updating business: {str(e)}\033[0m")

        # Option 4: Delete business
        elif choice == "4":
            try:
                print("\n\033[92mList of All Businesses:\033[0m")
                businesses = view_all("Business")
                if not businesses:
                    print("\033[93mNo businesses found to delete.\033[0m")
                    continue
                for b in businesses:
                    print(
                        f"\033[92mID:\033[0m {b[0]} "
                        f"\033[92mBusiness Name:\033[0m {b[1]} "
                        f"\033[92mEmail:\033[0m {b[2]} "
                        f"\033[92mPhone:\033[0m {b[3]} "
                        f"\033[92mAddress:\033[0m {b[4]} "
                        f"\033[92mDate of Registration:\033[0m {b[5]}"
                    )

                print("\033[93mTip: Please enter the ID number of the business you wish to delete.\033[0m")
                business_id = input("Enter Business ID to delete: ").strip()
                if not business_id.isdigit():
                    print("\033[91m🚫 Business ID must be numeric.\033[0m")
                    continue

                if has_linked_donations("Business_ID", business_id):
                    print("\033[91m🚫 Cannot delete Business linked to existing Donations.\033[0m")
                    continue

                delete_entry("DELETE FROM Business WHERE Business_ID=?", business_id)
                print("\033[92m🎉 Business deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error deleting business: {str(e)}\033[0m")

        # Option 5: Exit to main menu
        elif choice == "5":
            break

if __name__ == "__main__":
    business_menu()
