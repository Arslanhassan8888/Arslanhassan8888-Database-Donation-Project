# business.py 
import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module handles all business-related operations in the donation system.
It provides a menu interface for managing business records including:
- Viewing all businesses
- Adding new businesses
- Updating existing businesses
- Deleting businesses (with donation checks)
"""

from start.crud import view_all, add_entry, update_entry, delete_entry, linked_donations

def display_businesses(businesses):
    """Display all business records in a consistent format"""
    if not businesses:
        print("\033[93mNo businesses found in database.\033[0m")
        return False
    for i in businesses:
        print(
            f"\033[92mID:\033[0m {i[0]} "
            f"\033[92mName:\033[0m {i[1]} "
            f"\033[92mEmail:\033[0m {i[2]} "
            f"\033[92mPhone:\033[0m {i[3]} "
            f"\033[92mAddress:\033[0m {i[4]} "
            f"\033[92mRegistration Date:\033[0m {i[5]}"
        )
    return True

def business_input(action):
    """Collect and validate business information from user"""
    print("\n\033[93mTip: Business Name should only contain letters.\033[0m")
    name = input(f"{action} Business Name: ").strip()
    if not name.replace(" ", "").isalpha():
        print("\033[91m🚫 Business name must contain only letters.\033[0m")
        return None
    name = name.capitalize()

    print("\033[93mTip: Use a valid email address (e.g., name@business.com).\033[0m")
    email = input(f"{action} Email: ").strip()
    if "@" not in email or "." not in email:# Check for basic email format This is a simple check; consider using regex for more complex validation
        print("\033[91m🚫 Please enter a valid email address.\033[0m")
        return None

    print("\033[93mTip: Phone number must be digits only.\033[0m")
    phone = input(f"{action} Phone Number (digits only): ").strip()
    if not phone.isdigit():
        print("\033[91m🚫 Phone number must contain only digits.\033[0m")
        return None

    print("\033[93mTip: Address cannot be empty.\033[0m")
    address = input(f"{action} Address: ").strip()

    print("\033[93mTip: Use format YYYY-MM-DD for Date of Registration.\033[0m") 
    reg_date = input(f"{action} Date of Registration (YYYY-MM-DD): ").strip()# Check for date format YYYY-MM-DD
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", reg_date): # Regex to check date format 
        print("\033[91m🚫 Date must be in format YYYY-MM-DD.\033[0m")
        return None

    return (name, email, phone, address, reg_date)

def business_menu():
    """
    Main business management interface
    Handles all CRUD operations for businesses through a menu system
    """
    while True:
        # Display menu options
        print("\n" + "🎯  BUSINESS MANAGEMENT MENU  🎯".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  View All Businesses")
        print("2️⃣  Add Business")
        print("3️⃣  Update Business")
        print("4️⃣  Delete Business")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n Choose an option (1-5): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91m🚫 Invalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        # View all businesses
        if choice == "1":
            try:
                print("\n\033[92mAll Businesses:\033[0m")
                businesses = view_all("Business")
                display_businesses(businesses)
            except Exception as e:
                print(f"\033[91m🚫 Error viewing businesses: {str(e)}\033[0m")

        # Add new business
        elif choice == "2":
            try:
                data = business_input("Add")
                if data:
                    add_entry(
                        "INSERT INTO Business VALUES (NULL,?,?,?,?,?)",
                        data
                    )
                    print("\033[92m🎉 Business added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error adding business: {str(e)}\033[0m")

        # Update existing business
        elif choice == "3":
            try:
                print("\n\033[92mList of All Businesses:\033[0m")
                businesses = view_all("Business")
                if not display_businesses(businesses):
                    continue

                business_id = input("\nEnter Business ID to update: ").strip()
                if not business_id.isdigit():
                    print("\033[91m🚫 Business ID must be numeric.\033[0m")
                    continue

                data = business_input("New")
                if data:
                    update_entry(
                        "UPDATE Business SET Name=?, Email=?, Phone_Number=?, Address=?, Registration_Date=? WHERE Business_ID=?",
                        (*data, business_id)
                    )
                    print("\033[92m🎉 Business updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error updating business: {str(e)}\033[0m")

        # Delete business
        elif choice == "4":
            try:
                print("\n\033[92mList of All Businesses:\033[0m")
                businesses = view_all("Business")
                if not display_businesses(businesses):
                    continue

                business_id = input("\nEnter Business ID to delete: ").strip()
                if not business_id.isdigit():
                    print("\033[91m🚫 Business ID must be numeric.\033[0m")
                    continue

                if linked_donations("Business_ID", business_id):
                    print("\033[91m🚫 Cannot delete Business linked to existing Donations.\033[0m")
                    continue

                delete_entry("DELETE FROM Business WHERE Business_ID=?", business_id)
                print("\033[92m🎉 Business deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error deleting business: {str(e)}\033[0m")

        # Return to main menu
        elif choice == "5":
            break

if __name__ == "__main__":
    business_menu()