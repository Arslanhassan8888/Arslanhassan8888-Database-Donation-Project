# donation.py 
import sys
import os
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module handles all donation-related operations in the system.
It provides a menu interface for managing donation records including:
- Viewing all donations
- Adding new donations
- Updating existing donations
- Deleting donations
"""

from start.crud import view_all, add_entry, update_entry, delete_entry

def display_donations(donations): # Display all donation records in a consistent format
    if not donations: # Check if the donations list is empty. If empty, print a message and return False
        print("\033[93mNo donations found in database.\033[0m")
        return False
    for d in donations: # Iterate through each donation record in the donations list Print the details of each donation record in a formatted manner
        print(
            f"\033[92mID:\033[0m {d[0]} "
            f"\033[92mAmount:\033[0m £{d[1]:,.2f} "
            f"\033[92mDate:\033[0m {d[2]} "
            f"\033[92mNotes:\033[0m {d[3]} "
            f"\033[92mDonor ID:\033[0m {d[4] if d[4] else 'None'} "
            f"\033[92mEvent ID:\033[0m {d[5] if d[5] else 'None'} "
            f"\033[92mBusiness ID:\033[0m {d[6] if d[6] else 'None'} "
            f"\033[92mBeneficiary ID:\033[0m {d[7]}"
        )
    return True

def donation_input(action, display_entities=True):# Collect and validate donation information from user 
    if display_entities:# Display available entities if the flag is set to True
        print("\n\033[93mTip: Choose one sender ID (Donor, Event, or Business) and one Beneficiary ID.\033[0m")

    donor_id = input(f"{action} Donor ID (leave blank if not applicable): ").strip() # Check if the user wants to input a donor ID
    event_id = input(f"{action} Event ID (leave blank if not applicable): ").strip() # Check if the user wants to input an event ID
    business_id = input(f"{action} Business ID (leave blank if not applicable): ").strip()# Check if the user wants to input a business ID
    beneficiary_id = input(f"{action} Beneficiary ID: ").strip() # Check if the user wants to input a beneficiary ID

    if not beneficiary_id.isdigit(): # Check if the beneficiary ID is a number # If not, print an error message and return None
        print("\033[91m🚫 Beneficiary ID must be a number.\033[0m")
        return None

    if donor_id and not donor_id.isdigit():
        print("\033[91m🚫 Donor ID must be numeric if provided.\033[0m")
        return None
    if event_id and not event_id.isdigit():
        print("\033[91m🚫 Event ID must be numeric if provided.\033[0m")
        return None
    if business_id and not business_id.isdigit():
        print("\033[91m🚫 Business ID must be numeric if provided.\033[0m")
        return None

    print("\033[93mTip: Enter a valid positive amount (e.g., 100.50)\033[0m")
    amount_input = input(f"{action} Donation Amount: ").strip()
    try:
        amount = float(amount_input) # Convert the input to a float. Check if the amount is a valid positive number
        if amount <= 0: # If the amount is not positive, raise a ValueError
            raise ValueError("Amount must be positive")
    except ValueError: # If the conversion fails or the amount is not positive, print an error message and return Non
        print("\033[91m🚫 Invalid amount. Must be a positive number.\033[0m")
        return None

    print("\033[93mTip: Use the format YYYY-MM-DD for the donation date.\033[0m")
    date = input(f"{action} Date (YYYY-MM-DD): ").strip() # Check if the date is in the correct format YYYY-MM-DD
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date): # Regex to check date format If the date is not in the correct format, print an error message and return None
        print("\033[91m🚫 Date must be in format YYYY-MM-DD.\033[0m")
        return None

    notes = input(f"{action} Notes (optional): ").strip()

    return ( # Return a tuple containing the collected data # The tuple includes the amount, date, notes, and IDs for donor, event, business, and beneficiary
        amount, date, notes, 
        donor_id or None, 
        event_id or None, 
        business_id or None, 
        beneficiary_id
    )

def donation_menu():
    """
    Main donation management interface
    Handles all CRUD operations for donations through a menu system
    """
    while True:
        # Display menu options
        print("\n" + "🎯  DONATION MANAGEMENT MENU  🎯".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  View All Donations")
        print("2️⃣  Add Donation")
        print("3️⃣  Update Donation")
        print("4️⃣  Delete Donation")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n Choose an option (1-5): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91m🚫 Invalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        # View all donations
        if choice == "1":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation")
                display_donations(donations)
            except Exception as e:
                print(f"\033[91m🚫 Error viewing donations: {str(e)}\033[0m")

        # Add new donation
        elif choice == "2":
            try:
                # Display available entities directly in the menu
                print("\n\033[92mAvailable Donors:\033[0m")
                donors = view_all("Donor")
                for donor in donors:
                    print(f"\033[92mID:\033[0m {donor[0]} \033[92mName:\033[0m {donor[1]} {donor[2]}")

                print("\n\033[92mAvailable Events:\033[0m")
                events = view_all("Event")
                for event in events:
                    print(f"\033[92mID:\033[0m {event[0]} \033[92mName:\033[0m {event[1]}")

                print("\n\033[92mAvailable Businesses:\033[0m")
                businesses = view_all("Business")
                for business in businesses:
                    print(f"\033[92mID:\033[0m {business[0]} \033[92mName:\033[0m {business[1]}")

                print("\n\033[92mAvailable Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary")
                for beneficiary in beneficiaries:
                    print(f"\033[92mID:\033[0m {beneficiary[0]} \033[92mName:\033[0m {beneficiary[1]}")

                data = donation_input("Add", display_entities=False)
                if data:
                    add_entry(
                        """INSERT INTO Donation 
                        (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) 
                        VALUES (?,?,?,?,?,?,?)""",
                        data
                    )
                    print("\033[92m🎉 Donation recorded successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error adding donation: {str(e)}\033[0m")

        # Update existing donation
        elif choice == "3":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation")
                if not display_donations(donations):
                    continue

                donation_id = input("\nEnter Donation ID to update: ").strip()
                if not donation_id.isdigit():
                    print("\033[91m🚫 Donation ID must be a number.\033[0m")
                    continue

                # Display available entities directly in the menu
                print("\n\033[92mAvailable Donors:\033[0m")
                donors = view_all("Donor")
                for donor in donors:
                    print(f"\033[92mID:\033[0m {donor[0]} \033[92mName:\033[0m {donor[1]} {donor[2]}")

                print("\n\033[92mAvailable Events:\033[0m")
                events = view_all("Event")
                for event in events:
                    print(f"\033[92mID:\033[0m {event[0]} \033[92mName:\033[0m {event[1]}")

                print("\n\033[92mAvailable Businesses:\033[0m")
                businesses = view_all("Business")
                for business in businesses:
                    print(f"\033[92mID:\033[0m {business[0]} \033[92mName:\033[0m {business[1]}")

                print("\n\033[92mAvailable Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary")
                for beneficiary in beneficiaries:
                    print(f"\033[92mID:\033[0m {beneficiary[0]} \033[92mName:\033[0m {beneficiary[1]}")

                data = donation_input("New", display_entities=False)
                if data:
                    update_entry(
                        """UPDATE Donation 
                        SET Amount=?, Date=?, Notes=?, Donor_ID=?, Event_ID=?, Business_ID=?, Beneficiary_ID=? 
                        WHERE Donation_ID=?""",
                        (*data, donation_id)
                    )
                    print("\033[92m🎉 Donation updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error updating donation: {str(e)}\033[0m")

        # Delete donation
        elif choice == "4":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation")
                if not display_donations(donations):
                    continue

                donation_id = input("\nEnter Donation ID to delete: ").strip()
                if not donation_id.isdigit():
                    print("\033[91m🚫 Donation ID must be numeric.\033[0m")
                    continue

                delete_entry("DELETE FROM Donation WHERE Donation_ID=?", donation_id)
                print("\033[92m🎉 Donation deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error deleting donation: {str(e)}\033[0m")

        # Return to main menu
        elif choice == "5":
            break

if __name__ == "__main__":
    donation_menu()
