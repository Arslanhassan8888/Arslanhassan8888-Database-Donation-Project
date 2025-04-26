# beneficiary.py 

import sys # Importing sys for system-specific parameters and functions
import os # Importing os for operating system dependent functionality
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # This allows us to import modules from the parent directory

"""
This module handles all beneficiary-related operations in the donation system.
It provides a menu interface for managing beneficiary records including:
- Viewing all beneficiaries
- Adding new beneficiaries
- Updating existing beneficiaries
- Deleting beneficiaries (with donation checks)

"""

from start.crud import view_all, add_entry, update_entry, delete_entry, linked_donations

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

        # Ask user to choose an option
        choice = input("\n Choose an option (1-5): ").strip()

        # Validate input
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]: 
            print("\033[91m🚫 Invalid entry. Please choose an option between (1-5).\033[0m")
            continue

        # Option 1: View all beneficiaries
        if choice == "1":
            try:
                print("\n\033[92mAll Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary") # Fetch all beneficiaries from the database
                if not beneficiaries:# Check if the list is empty
                    print("\033[93mNo beneficiaries found in database.\033[0m")
                else:
                    for b in beneficiaries:# Loop through each beneficiary and print their details
                        print(
                            f"\033[92mID:\033[0m {b[0]} "
                            f"\033[92mName:\033[0m {b[1]} "
                            f"\033[92mType:\033[0m {b[2]} "
                            f"\033[92mAddress:\033[0m {b[3]} "
                            f"\033[92mSupport Duration:\033[0m {b[4]} "
                            f"\033[92mFunding Priority:\033[0m {b[5]}"
                        )
            except Exception as e:
                print(f"\033[91m🚫 An error occurred while viewing beneficiaries: {e}\033[0m")

        # Option 2: Add new beneficiary
        elif choice == "2":
            try:
                print("\n\033[93mTip: Name and Type should contain only letters.\033[0m")
                name = input("Name (letters only): ").strip()# Strip any leading/trailing whitespace
                if not name.replace(" ", "").isalpha():# Check if name contains only letters and spaces
                    # If not, print an error message and continue to the next iteration of the loop
                    # This prevents the program from crashing and allows the user to correct their input
                    print("\033[91m🚫 Name must contain only letters.\033[0m")
                    continue
                name = name.capitalize()# Capitalize the first letter of the name

                print("\033[93mTip: Type should also include only letters (e.g., Charity, Non-Profit).\033[0m")
                btype = input("Type (e.g., Charity, Non-Profit): ").strip()
                if not btype.replace(" ", "").isalpha():
                    print("\033[91m🚫 Type must contain only letters.\033[0m")
                    continue

                print("\033[93mTip: Enter the full address of the organisation.\033[0m")
                address = input("Address (e.g., 123 Main St, Springfield): ").strip()

                duration = input("Support Duration (e.g., 5 years): ").strip()

                print("\033[93mTip: Enter High, Medium, or Low as priority.\033[0m")
                priority = input("Priority (High, Medium, Low): ").strip().capitalize()
                if not priority.isalpha():
                    print("\033[91m🚫 Priority must contain only letters.\033[0m")
                    continue

                add_entry(
                    "INSERT INTO Beneficiary VALUES (NULL,?,?,?,?,?)",  # Insert new beneficiary into the database
                    # The NULL value is used for the ID, which is auto-incremented by the database
                    (name, btype, address, duration, priority)  # Tuple containing the values to be inserted  The values are passed as a tuple to prevent SQL injection attacks
                )
                print("\033[92m🎉 Beneficiary added successfully.\033[0m")
            except Exception as e: # Catch any exceptions that occur during the database operation
                print(f"\033[91m🚫 An error occurred while adding the beneficiary: {e}\033[0m")

        # Option 3: Update existing beneficiary
        elif choice == "3":
            try:
                print("\n\033[92mAll Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary")
                if not beneficiaries:
                    print("\033[93mNo beneficiaries found to update.\033[0m")
                    continue
                for b in beneficiaries:
                    print(
                        f"\033[92mID:\033[0m {b[0]} "
                        f"\033[92mName:\033[0m {b[1]} "
                        f"\033[92mType:\033[0m {b[2]} "
                        f"\033[92mAddress:\033[0m {b[3]} "
                        f"\033[92mSupport Duration:\033[0m {b[4]} "
                        f"\033[92mFunding Priority:\033[0m {b[5]}"
                    )

                print("\n\033[93mTip: Please enter the ID of Beneficiary you wish to update.\033[0m")
                bid = input("Enter Beneficiary ID to update: ").strip() 
                if not bid.isdigit(): # Check if the input is a digit
                    print("\033[91m🚫 Beneficiary ID must be a number.\033[0m")
                    continue

                print("\033[93mTip: Name and Type must only contain letters.\033[0m")
                name = input("New Name: ").strip()
                if not name.replace(" ", "").isalpha():
                    print("\033[91m🚫 Name must contain only letters.\033[0m")
                    continue
                name = name.capitalize()

                btype = input("New Type: ").strip()
                if not btype.replace(" ", "").isalpha():
                    print("\033[91m🚫 Type must contain only letters.\033[0m")
                    continue

                print("\033[93mTip: Update the address if needed.\033[0m")
                address = input("New Address: ").strip()

                print("\033[93mTip: Duration can be '3 years', 'Ongoing', etc.\033[0m")
                duration = input("New Duration: ").strip()

                print("\033[93mTip: Enter High, Medium, or Low for new priority.\033[0m")
                priority = input("New Priority (High, Medium, Low): ").strip().capitalize()
                if not priority.isalpha():
                    print("\033[91m🚫 Priority must contain only letters.\033[0m")
                    continue

                update_entry(
                    "UPDATE Beneficiary SET Name=?, Type=?, Address=?, Support_Duration=?, Funding_priority=? WHERE Beneficiary_ID=?",
                    (name, btype, address, duration, priority, bid)
                )
                print("\033[92m🎉 Beneficiary updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 An error occurred while updating the beneficiary: {e}\033[0m")

        # Option 4: Delete a beneficiary
        elif choice == "4":
            try:
                print("\n\033[92mAll Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary")
                if not beneficiaries:
                    print("\033[93mNo beneficiaries found to delete.\033[0m")
                    continue
                for b in beneficiaries:
                    print(
                        f"\033[92mID:\033[0m {b[0]} "
                        f"\033[92mName:\033[0m {b[1]} "
                        f"\033[92mType:\033[0m {b[2]} "
                        f"\033[92mAddress:\033[0m {b[3]} "
                        f"\033[92mSupport Duration:\033[0m {b[4]} "
                        f"\033[92mFunding Priority:\033[0m {b[5]}"
                    )

                print("\n\033[93mTip: Please enter the ID of Beneficiary you wish to delete.\033[0m")
                bid = input("Enter Beneficiary ID to delete: ").strip()
                if not bid.isdigit():
                    print("\033[91m🚫 Beneficiary ID must be numeric.\033[0m")
                    continue

                if linked_donations("Beneficiary_ID", bid): # Check if the beneficiary has linked donations
                    # If yes, print an error message and continue to the next iteration of the loop
                    print("\033[91m🚫 Cannot delete Beneficiary linked to existing Donations.\033[0m")
                    continue

                delete_entry("DELETE FROM Beneficiary WHERE Beneficiary_ID=?", bid) # Delete the beneficiary from the database
                # The ID is passed as a parameter to prevent SQL injection attacks 
                print("\033[92m🎉 Beneficiary deleted successfully.\033[0m")
            except Exception as e: # Catch any exceptions that occur during the database operation
                print(f"\033[91m🚫 An error occurred while deleting the beneficiary: {e}\033[0m")

        # Option 5: Return to main menu
        elif choice == "5":
            break

if __name__ == "__main__": # If this script is run directly, call the beneficiary_menu function to start the program
    beneficiary_menu()
