# beneficiary.py
# Import functions for database operations (viewing, adding, updating, deleting)
from start.crud import view_all, add_entry, update_entry, delete_entry
# Import function to connect to the database
from start.tables import get_connection

"""
This module handles all beneficiary-related operations in the donation system.
It provides a menu interface for managing beneficiary records including:
- Viewing all beneficiaries
- Adding new beneficiaries
- Updating existing beneficiaries
- Deleting beneficiaries
"""

def beneficiary_menu():
    """
    Displays and manages the beneficiary management menu.
    This is the main interface for all beneficiary operations.
    Uses a continuous loop to keep showing the menu until user exits.
    """
    while True:
        # Print menu options in green colour
        print("\n\033[92m--- Beneficiary Management ---\033[0m", flush=True)
        print("1. View All Beneficiaries")
        print("2. Add Beneficiary")
        print("3. Update Beneficiary")
        print("4. Delete Beneficiary")
        print("5. Back to Main Menu")

        # Ask user to choose an option, where "strip" remove extra spaces
        choice = input("\033[92mChoose an option (1-5): \033[0m").strip()

        # If user enters something that's not a digit or not in the list, show error
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91mInvalid entry. Please choose an option between (1-5).\033[0m")
            continue

        # Option 1: View all beneficiaries
        """
        "view_all" is imported from crud.py. it retrieve all the tables, but in this case we are specifing the parameter to get only beneficary table for this action
        "return result" of the function will result all details of the table in form of a list tuples. Then the loop will iterate through each element of the list, where
        "b" is used for the iteration and [1] is the index position 1 where is name and so on where the other elements. for example at index [1] it will print out
        name: children foundation .
        note at index[0] there are ID which i don't want to print
        """
        if choice == "1":
            try:
                print("\n\033[92mAll Beneficiaries:\033[0m")#\n adds a blank line before the text for better spacing.
                # Call view_all function with "Beneficiary" table name
                for b in view_all("Beneficiary"):
                    print(
                        f"\033[92mName:\033[0m {b[1]} "
                        f"\033[92mType:\033[0m {b[2]} "
                        f"\033[92mAddress:\033[0m {b[3]} "
                        f"\033[92mSupport Duration:\033[0m {b[4]} "
                        f"\033[92mFunding Priority:\033[0m {b[5]}"
                    )
            except Exception as e:
                # If there's an error while fetching data, show the error message
                print(f"\033[91mAn error occurred while viewing beneficiaries: {e}\033[0m")

        # Option 2: Add new beneficiary
        elif choice == "2":
            try:
                print("\033[93mTip: Name and Type should contain only letters.\033[0m")
                name = input("Name (letters only): ").strip() 
                if not name.replace(" ", "").isalpha():
                    print("\033[91mName must contain only letters.\033[0m")
                    continue     
                name = name.capitalize()

                btype = input("Type (e.g., Charity, Non-Profit): ").strip()
                if not btype.replace(" ", "").isalpha():
                    print("\033[91mType must contain only letters.\033[0m")
                    continue

                print("\033[93mTip: Enter the full address of the organisation.\033[0m")
                address = input("Address (e.g., 123 Main St, Springfield): ").strip()
                duration = input("Support Duration (e.g., 5 years): ").strip()

                print("\033[93mTip: Enter High, Medium, or Low as priority.\033[0m")
                priority = input("Priority (High, Medium, Low): ").strip().capitalize()
                if not priority.isalpha():
                    print("\033[91mPriority must contain only letters.\033[0m")
                    continue

                # Insert new beneficiary into the database
                add_entry(
                    "INSERT INTO Beneficiary VALUES (NULL,?,?,?,?,?)",
                    (name, btype, address, duration, priority)
                )
                print("\033[92mBeneficiary added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mAn error occurred while adding the beneficiary: {e}\033[0m")

       # Option 3: Update existing beneficiary
        elif choice == "3":
            try:
                print("\033[93mTip: Make sure to enter the correct Beneficiary ID you want to update.\033[0m")
                bid = input("Enter Beneficiary ID to update: ").strip()
                if not bid.isdigit():
                    print("\033[91mBeneficiary ID must be a number.\033[0m")
                    continue

                print("\033[93mTip: Name and Type must only contain letters.\033[0m")
                name = input("New Name: ").strip()
                if not name.replace(" ", "").isalpha():
                    print("\033[91mName must contain only letters.\033[0m")
                    continue
                name = name.capitalize()

                btype = input("New Type: ").strip()
                if not btype.replace(" ", "").isalpha():
                    print("\033[91mType must contain only letters.\033[0m")
                    continue

                print("\033[93mTip: Fill in updated address and duration details.\033[0m")
                address = input("New Address: ").strip()
                duration = input("New Duration: ").strip()

                print("\033[93mTip: Enter High, Medium, or Low for new priority.\033[0m")
                priority = input("New Priority (High, Medium, Low): ").strip().capitalize()
                if not priority.isalpha():
                    print("\033[91mPriority must contain only letters.\033[0m")
                    continue

                update_entry(
                    "UPDATE Beneficiary SET Name=?, Type=?, Address=?, Support_Duration=?, Funding_priority=? WHERE Beneficiary_ID=?",
                    (name, btype, address, duration, priority, bid)
                )
                print("\033[92mBeneficiary updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mAn error occurred while updating the beneficiary: {e}\033[0m")

        # option 4 :Delete a beneficiary
        elif choice == "4":
            try:
                print("\033[93mTip: Deleting a beneficiary will also remove any donations linked to them.\033[0m")
                bid = input("Enter Beneficiary ID to delete: ").strip()
                if not bid.isdigit():
                    print("\033[91mBeneficiary ID must be a number.\033[0m")
                    continue
                
                delete_entry("DELETE FROM Beneficiary WHERE Beneficiary_ID=?", bid)
                print("\033[92mBeneficiary and all related donations deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mAn error occurred while deleting the beneficiary: {e}\033[0m")

        # option 5: Return to the main menu
        elif choice == "5":
            break

# If this file is run directly (not imported), run the menu
if __name__ == "__main__":
    beneficiary_menu()
