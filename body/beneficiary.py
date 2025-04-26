# beneficiary.py 

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module handles all beneficiary-related operations in the donation system.
It provides a menu interface for managing beneficiary records including:
- Viewing all beneficiaries
- Adding new beneficiaries
- Updating existing beneficiaries
- Deleting beneficiaries (with donation checks)
"""

from start.crud import view_all, add_entry, update_entry, delete_entry, linked_donations

def display_beneficiaries(beneficiaries):# Display all beneficiary records in a consistent format
    if not beneficiaries:
        print("\033[93mNo beneficiaries found in database.\033[0m")
        return False
    for i in beneficiaries:
        print(
            f"\033[92mID:\033[0m {i[0]} "
            f"\033[92mName:\033[0m {i[1]} "
            f"\033[92mType:\033[0m {i[2]} "
            f"\033[92mAddress:\033[0m {i[3]} "
            f"\033[92mSupport Duration:\033[0m {i[4]} "
            f"\033[92mFunding Priority:\033[0m {i[5]}"
        )
    return True

def beneficiary_input(action):# Collect and validate beneficiary information from user
    print(f"\n\033[93mTip: Name and Type should contain only letters.\033[0m")
    name = input(f"{action} Name (letters only): ").strip()
    if not name.replace(" ", "").isalpha():# Check if name contains only letters and spaces
        print("\033[91m🚫 Name must contain only letters.\033[0m")
        return None# Return None if invalid input is detected
    name = name.capitalize() # Capitalize the first letter of the name

    print("\033[93mTip: Type should also include only letters (e.g., Charity, Non-Profit).\033[0m")
    btype = input(f"{action} Type (e.g., Charity, Non-Profit): ").strip()
    if not btype.replace(" ", "").isalpha():
        print("\033[91m🚫 Type must contain only letters.\033[0m")
        return None

    print("\033[93mTip: Enter the full address of the organisation.\033[0m")
    address = input(f"{action} Address (e.g., 123 Main St, Springfield): ").strip()

    duration = input(f"{action} Support Duration (e.g., 5 years): ").strip()

    print("\033[93mTip: Enter High, Medium, or Low as priority.\033[0m")
    priority = input(f"{action} Priority (High, Medium, Low): ").strip().capitalize()
    if not priority.isalpha():
        print("\033[91m🚫 Priority must contain only letters.\033[0m")
        return None

    return (name, btype, address, duration, priority)

def beneficiary_menu():
    """
    Displays and manages the beneficiary management menu.
    This is the main interface for all beneficiary operations.
    Uses a continuous loop to keep showing the menu until user exits.
    """
    while True:
        # Print menu options with decoration
        print("\n" + "🎯  BENEFICIARY MANAGEMENT MENU  🎯".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  View All Beneficiaries")
        print("2️⃣  Add Beneficiary")
        print("3️⃣  Update Beneficiary")
        print("4️⃣  Delete Beneficiary")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n Choose an option (1-5): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]: 
            print("\033[91m🚫 Invalid entry. Please choose an option between (1-5).\033[0m")
            continue

        # Option 1: View all beneficiaries
        if choice == "1":
            try:
                print("\n\033[92mAll Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary")
                display_beneficiaries(beneficiaries)
            except Exception as e:
                print(f"\033[91m🚫 An error occurred while viewing beneficiaries: {e}\033[0m")

        # Option 2: Add new beneficiary
        elif choice == "2":
            try:
                data = beneficiary_input("Add") # Collect beneficiary data from user
                if data: # Check if data is valid
                            # Insert new beneficiary into the database
                    add_entry(
                        "INSERT INTO Beneficiary VALUES (NULL,?,?,?,?,?)",
                        data
                    )
                    print("\033[92m🎉 Beneficiary added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 An error occurred while adding the beneficiary: {e}\033[0m")

        # Option 3: Update existing beneficiary
        elif choice == "3":
            try:
                print("\n\033[92mAll Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary")# Display all beneficiaries
                if not display_beneficiaries(beneficiaries):# If no beneficiaries are found, exit the loop
                    continue

                bid = input("\nEnter Beneficiary ID to update: ").strip()
                if not bid.isdigit():
                    print("\033[91m🚫 Beneficiary ID must be a number.\033[0m")
                    continue

                data = beneficiary_input("New")
                if data:
                    update_entry(
                        "UPDATE Beneficiary SET Name=?, Type=?, Address=?, Support_Duration=?, Funding_priority=? WHERE Beneficiary_ID=?",
                        (*data, bid)
                    )
                    print("\033[92m🎉 Beneficiary updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 An error occurred while updating the beneficiary: {e}\033[0m")

        # Option 4: Delete a beneficiary
        elif choice == "4":
            try:
                print("\n\033[92mAll Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary")
                if not display_beneficiaries(beneficiaries):# If no beneficiaries are found, exit the loop
                    continue 

                bid = input("\nEnter Beneficiary ID to delete: ").strip()# Check if the ID is numeric
                if not bid.isdigit():
                    print("\033[91m🚫 Beneficiary ID must be numeric.\033[0m")
                    continue

                if linked_donations("Beneficiary_ID", bid): # Check if the beneficiary is linked to any donations
                    print("\033[91m🚫 Cannot delete Beneficiary linked to existing Donations.\033[0m")
                    continue # If linked, skip deletion 

                delete_entry("DELETE FROM Beneficiary WHERE Beneficiary_ID=?", bid)# Delete the beneficiary from the database
                print("\033[92m🎉 Beneficiary deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 An error occurred while deleting the beneficiary: {e}\033[0m")

        # Option 5: Return to main menu
        elif choice == "5":
            break

if __name__ == "__main__":
    beneficiary_menu()