# donation.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#In this page i used the same crud concept explained for beneficiary.py view, create,update and delete with minor changes
"""
This module handles all donation-related operations in the system.
It provides a menu interface for managing donation records including:
- Viewing all donations
- Adding new donations
- Updating existing donations
- Deleting donations
"""

import re  # For date validation
from start.crud import view_all, add_entry, update_entry, delete_entry

def donation_menu():
    """
    Displays and manages the donation management menu.
    Provides continuous interface for donation operations until user exits.
    Handles all CRUD operations for donation records with validation.
    """
    while True:
        # Display menu options with green header
        print("\n\033[92m--- Donation Management ---\033[0m", flush=True)
        print("1. View All Donations")
        print("2. Add Donation")
        print("3. Update Donation")
        print("4. Delete Donation")
        print("5. Back to Main Menu")
        
        # Get and validate menu choice
        choice = input("\033[92mChoose an option (1-5): \033[0m").strip()
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91mInvalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        # Option 1: View all donations
        if choice == "1":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation")
                if not donations:
                    print("\033[93mNo donations found in database.\033[0m")
                else:
                    for d in donations:
                        print(
                            f"\033[92mDonation ID:\033[0m {d[0]} "
                            f"\033[92mAmount:\033[0m £{d[1]:,.2f} "
                            f"\033[92mDate:\033[0m {d[2]} "
                            f"\033[92mDonor:\033[0m {d[4]} "
                            f"\033[92mBeneficiary:\033[0m {d[5]}"
                        )
            except Exception as e:
                print(f"\033[91mError viewing donations: {str(e)}\033[0m")

        # Option 2: Add new donation
        elif choice == "2":
            try:
                donor_id = input("Donor ID: ").strip()
                if not donor_id.isdigit():
                    print("\033[91mDonor ID must be a number.\033[0m")
                    continue

                beneficiary_id = input("Beneficiary ID: ").strip()
                if not beneficiary_id.isdigit():
                    print("\033[91mBeneficiary ID must be a number.\033[0m")
                    continue

                event_id = input("Event ID (leave blank if none): ").strip()
                if event_id and not event_id.isdigit():
                    print("\033[91mEvent ID must be a number.\033[0m")
                    continue

                volunteer_id = input("Volunteer ID (leave blank if none): ").strip()
                if volunteer_id and not volunteer_id.isdigit():
                    print("\033[91mVolunteer ID must be a number.\033[0m")
                    continue

                amount_input = input("Donation Amount: ").strip()
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        raise ValueError("Amount must be positive")
                except ValueError:
                    print("\033[91mInvalid amount. Must be a positive number.\033[0m")
                    continue

                date = input("Date (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("\033[91mDate must be in format YYYY-MM-DD.\033[0m")
                    continue

                notes = input("Notes (optional): ").strip()

                add_entry(
                    "INSERT INTO Donation (Donor_ID, Beneficiary_ID, Event_ID, Volunteer_ID, Amount, Date, Notes) VALUES (?,?,?,?,?,?,?)",
                    (donor_id, beneficiary_id, event_id or None, volunteer_id or None, amount, date, notes)
                )
                print("\033[92mDonation recorded successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError adding donation: {str(e)}\033[0m")

        # Option 3: Update donation
        elif choice == "3":
            try:
                donation_id = input("Enter Donation ID to update: ").strip()
                if not donation_id.isdigit():
                    print("\033[91mDonation ID must be a number.\033[0m")
                    continue

                donor_id = input("Donor ID: ").strip()
                if not donor_id.isdigit():
                    print("\033[91mDonor ID must be a number.\033[0m")
                    continue

                beneficiary_id = input("Beneficiary ID: ").strip()
                if not beneficiary_id.isdigit():
                    print("\033[91mBeneficiary ID must be a number.\033[0m")
                    continue

                event_id = input("Event ID (leave blank if none): ").strip()
                if event_id and not event_id.isdigit():
                    print("\033[91mEvent ID must be a number.\033[0m")
                    continue

                volunteer_id = input("Volunteer ID (leave blank if none): ").strip()
                if volunteer_id and not volunteer_id.isdigit():
                    print("\033[91mVolunteer ID must be a number.\033[0m")
                    continue

                amount_input = input("Donation Amount: ").strip()
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        raise ValueError("Amount must be positive")
                except ValueError:
                    print("\033[91mInvalid amount. Must be a positive number.\033[0m")
                    continue

                date = input("Date (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("\033[91mDate must be in format YYYY-MM-DD.\033[0m")
                    continue

                notes = input("Notes (optional): ").strip()

                update_entry(
                    "UPDATE Donation SET Donor_ID=?, Beneficiary_ID=?, Event_ID=?, Volunteer_ID=?, Amount=?, Date=?, Notes=? WHERE Donation_ID=?",
                    (donor_id, beneficiary_id, event_id or None, volunteer_id or None, amount, date, notes, donation_id)
                )
                print("\033[92mDonation updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError updating donation: {str(e)}\033[0m")

        # Option 4: Delete donation
        elif choice == "4":
            try:
                donation_id = input("Enter Donation ID to delete: ").strip()
                if not donation_id.isdigit():
                    print("\033[91mDonation ID must be a number.\033[0m")
                    continue

                delete_entry("DELETE FROM Donation WHERE Donation_ID=?", donation_id)
                print("\033[92mDonation deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError deleting donation: {str(e)}\033[0m")

        # Option 5: Exit to main menu
        elif choice == "5":
            break

if __name__ == "__main__":
    donation_menu()
