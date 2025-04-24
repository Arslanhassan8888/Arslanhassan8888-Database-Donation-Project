# donation.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module handles all donation-related operations in the system.
It provides a menu interface for managing donation records including:
- Viewing all donations
- Adding new donations
- Updating existing donations
- Deleting donations
"""

import re
from start.crud import view_all, add_entry, update_entry, delete_entry

def donation_menu():
    while True:
        print("\n\033[92m--- Donation Management ---\033[0m", flush=True)
        print("1. View All Donations")
        print("2. Add Donation")
        print("3. Update Donation")
        print("4. Delete Donation")
        print("5. Back to Main Menu")

        choice = input("\033[92mChoose an option (1-5): \033[0m").strip()
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91mInvalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

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
                            f"\033[92mNotes:\033[0m {d[3]} "
                            f"\033[92mDonor ID:\033[0m {d[4]} "
                            f"\033[92mBeneficiary ID:\033[0m {d[5]} "
                            f"\033[92mEvent ID:\033[0m {d[6]} "
                            f"\033[92mVolunteer ID:\033[0m {d[7]}"
                        )
            except Exception as e:
                print(f"\033[91mError viewing donations: {str(e)}\033[0m")

        elif choice == "2":
            try:
                print("\n\033[93mTip: Donor, Beneficiary, Event, and Volunteer IDs must be valid numbers.\033[0m")
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

                print("\033[93mTip: Enter a valid amount like 100.50\033[0m")
                amount_input = input("Donation Amount: ").strip()
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        raise ValueError("Amount must be positive")
                except ValueError:
                    print("\033[91mInvalid amount. Must be a positive number.\033[0m")
                    continue

                print("\033[93mTip: Use the format YYYY-MM-DD for the donation date.\033[0m")
                date = input("Date (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("\033[91mDate must be in format YYYY-MM-DD.\033[0m")
                    continue

                notes = input("Notes (optional): ").strip()

                add_entry(
                    "INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Beneficiary_ID, Event_ID, Volunteer_ID) VALUES (?,?,?,?,?,?,?)",
                    (amount, date, notes, donor_id, beneficiary_id, event_id or None, volunteer_id or None)
                )
                print("\033[92mDonation recorded successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError adding donation: {str(e)}\033[0m")

        elif choice == "3":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation")
                for d in donations:
                    print(
                        f"\033[92mDonation ID:\033[0m {d[0]} "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f} "
                        f"\033[92mDate:\033[0m {d[2]} "
                        f"\033[92mDonor ID:\033[0m {d[4]} "
                        f"\033[92mBeneficiary ID:\033[0m {d[5]} "
                        f"\033[92mEvent ID:\033[0m {d[6]} "
                        f"\033[92mVolunteer ID:\033[0m {d[7]}"
                    )
                print("\n\033[93mTip: Enter the Donation ID you want to update.\033[0m")
                donation_id = input("Donation ID: ").strip()
                if not donation_id.isdigit():
                    print("\033[91mDonation ID must be a number.\033[0m")
                    continue

                # Repeat same validation steps for input fields as in Add
                # [You can copy the same validation block from above if needed for consistency]

            except Exception as e:
                print(f"\033[91mError updating donation: {str(e)}\033[0m")

        elif choice == "4":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation")
                for d in donations:
                    print(
                        f"\033[92mDonation ID:\033[0m {d[0]} "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f} "
                        f"\033[92mDate:\033[0m {d[2]} "
                        f"\033[92mDonor ID:\033[0m {d[4]} "
                        f"\033[92mBeneficiary ID:\033[0m {d[5]} "
                        f"\033[92mEvent ID:\033[0m {d[6]} "
                        f"\033[92mVolunteer ID:\033[0m {d[7]}"
                    )
                print("\n\033[93mTip: Enter the Donation ID you want to delete.\033[0m")
                donation_id = input("Enter Donation ID to delete: ").strip()
                if not donation_id.isdigit():
                    print("\033[91mDonation ID must be a number.\033[0m")
                    continue

                delete_entry("DELETE FROM Donation WHERE Donation_ID=?", donation_id)
                print("\033[92mDonation deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError deleting donation: {str(e)}\033[0m")

        elif choice == "5":
            break

if __name__ == "__main__":
    donation_menu()
