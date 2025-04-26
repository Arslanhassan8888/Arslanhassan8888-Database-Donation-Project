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
        # Print menu options with decoration
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

        # Option 1: View all donations
        if choice == "1":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation") # Fetch all donations
                if not donations: # Check if donations exist if no donations, print a message
                    print("\033[93mNo donations found in database.\033[0m")
                else:
                    for d in donations: # Loop through each donation and print details
                        # Format and print donation details with color coding
                        print(
                            f"\033[92mDonation ID:\033[0m {d[0]} "
                            f"\033[92mAmount:\033[0m £{d[1]:,.2f} "
                            f"\033[92mDate:\033[0m {d[2]} "
                            f"\033[92mNotes:\033[0m {d[3]} "
                            f"\033[92mDonor ID:\033[0m {d[4]} "
                            f"\033[92mEvent ID:\033[0m {d[5]} "
                            f"\033[92mBusiness ID:\033[0m {d[6]} "
                            f"\033[92mBeneficiary ID:\033[0m {d[7]}"
                        )
            except Exception as e: # Handle any exceptions that occur during the view operation
                print(f"\033[91m🚫 Error viewing donations: {str(e)}\033[0m")

        # Option 2: Add new donation
        elif choice == "2":
            try:
                # Print available Donors, Events, Businesses and Beneficiaries
                print("\n\033[92mAvailable Donors:\033[0m")
                donors = view_all("Donor") # Fetch all donors 
                for donor in donors: # Loop through each donor and print details
                    print(f"\033[92mDonor ID:\033[0m {donor[0]} \033[92mName:\033[0m {donor[1]} {donor[2]}")# Print donor ID and name
 
                print("\n\033[92mAvailable Events:\033[0m")
                events = view_all("Event")
                for event in events:
                    print(f"\033[92mEvent ID:\033[0m {event[0]} \033[92mName:\033[0m {event[1]}")

                print("\n\033[92mAvailable Businesses:\033[0m")
                businesses = view_all("Business")
                for business in businesses:
                    print(f"\033[92mBusiness ID:\033[0m {business[0]} \033[92mName:\033[0m {business[1]}")

                print("\n\033[92mAvailable Beneficiaries:\033[0m")
                beneficiaries = view_all("Beneficiary")
                for beneficiary in beneficiaries:
                    print(f"\033[92mBeneficiary ID:\033[0m {beneficiary[0]} \033[92mName:\033[0m {beneficiary[1]}")

                print("\n\033[93mTip: Choose one sender ID (Donor, Event, or Business) and one Beneficiary ID.\033[0m")

                donor_id = input("Donor ID (leave blank if not applicable): ").strip()
                event_id = input("Event ID (leave blank if not applicable): ").strip()
                business_id = input("Business ID (leave blank if not applicable): ").strip()
                beneficiary_id = input("Beneficiary ID: ").strip()

                if not beneficiary_id.isdigit(): # Check if beneficiary ID is numeric
                    # If not, print an error message and continue to the next iteration
                    print("\033[91m🚫 Beneficiary ID must be a number.\033[0m")
                    continue

                if donor_id and not donor_id.isdigit():
                    print("\033[91m🚫 Donor ID must be numeric if provided.\033[0m")
                    continue
                if event_id and not event_id.isdigit():
                    print("\033[91m🚫 Event ID must be numeric if provided.\033[0m")
                    continue
                if business_id and not business_id.isdigit():
                    print("\033[91m🚫 Business ID must be numeric if provided.\033[0m")
                    continue

                print("\033[93mTip: Enter a valid positive amount (e.g., 100.50)\033[0m")
                amount_input = input("Donation Amount: ").strip() # Prompt user for donation amount 
                try:
                    amount = float(amount_input) # Convert input to float
                    if amount <= 0:
                        raise ValueError("Amount must be positive")
                except ValueError:
                    print("\033[91m🚫 Invalid amount. Must be a positive number.\033[0m")
                    continue

                print("\033[93mTip: Use the format YYYY-MM-DD for the donation date.\033[0m")
                date = input("Date (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("\033[91m🚫 Date must be in format YYYY-MM-DD.\033[0m")
                    continue

                notes = input("Notes (optional): ").strip()

                add_entry(
                    "INSERT INTO Donation (Amount, Date, Notes, Donor_ID, Event_ID, Business_ID, Beneficiary_ID) VALUES (?,?,?,?,?,?,?)",
                    (amount, date, notes, donor_id or None, event_id or None, business_id or None, beneficiary_id)
                )
                print("\033[92m🎉 Donation recorded successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error adding donation: {str(e)}\033[0m")

        # Option 3: Update existing donation
        elif choice == "3":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation")
                if not donations:
                    print("\033[93mNo donations found to update.\033[0m")
                    continue
                for d in donations:
                    print(
                        f"\033[92mDonation ID:\033[0m {d[0]} "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f} "
                        f"\033[92mDate:\033[0m {d[2]} "
                        f"\033[92mNotes:\033[0m {d[3]} "
                        f"\033[92mDonor ID:\033[0m {d[4]} "
                        f"\033[92mEvent ID:\033[0m {d[5]} "
                        f"\033[92mBusiness ID:\033[0m {d[6]} "
                        f"\033[92mBeneficiary ID:\033[0m {d[7]}"
                    )

                print("\033[93mTip: Enter the Donation ID you want to update.\033[0m")
                donation_id = input("Donation ID: ").strip()
                if not donation_id.isdigit():
                    print("\033[91m🚫 Donation ID must be a number.\033[0m")
                    continue

                # Same as add donation flow
                donor_id = input("New Donor ID (leave blank if not applicable): ").strip()
                event_id = input("New Event ID (leave blank if not applicable): ").strip()
                business_id = input("New Business ID (leave blank if not applicable): ").strip()
                beneficiary_id = input("New Beneficiary ID: ").strip()

                if not beneficiary_id.isdigit():
                    print("\033[91m🚫 Beneficiary ID must be a number.\033[0m")
                    continue

                print("\033[93mTip: Enter a valid positive amount (e.g., 100.50)\033[0m")
                amount_input = input("New Donation Amount: ").strip()
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        raise ValueError("Amount must be positive")
                except ValueError:
                    print("\033[91m🚫 Invalid amount. Must be a positive number.\033[0m")
                    continue

                print("\033[93mTip: Use the format YYYY-MM-DD for the donation date.\033[0m")
                date = input("New Date (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("\033[91m🚫 Date must be in format YYYY-MM-DD.\033[0m")
                    continue

                notes = input("New Notes (optional): ").strip()

                update_entry(
                    "UPDATE Donation SET Amount=?, Date=?, Notes=?, Donor_ID=?, Event_ID=?, Business_ID=?, Beneficiary_ID=? WHERE Donation_ID=?",
                    (amount, date, notes, donor_id or None, event_id or None, business_id or None, beneficiary_id, donation_id)
                )
                print("\033[92m🎉 Donation updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error updating donation: {str(e)}\033[0m")

        # Option 4: Delete a donation
        elif choice == "4":
            try:
                print("\n\033[92mAll Donations:\033[0m")
                donations = view_all("Donation")
                if not donations:
                    print("\033[93mNo donations available to delete.\033[0m")
                    continue
                for d in donations:
                    print(
                        f"\033[92mDonation ID:\033[0m {d[0]} "
                        f"\033[92mAmount:\033[0m £{d[1]:,.2f} "
                        f"\033[92mDate:\033[0m {d[2]} "
                        f"\033[92mNotes:\033[0m {d[3]} "
                        f"\033[92mDonor ID:\033[0m {d[4]} "
                        f"\033[92mEvent ID:\033[0m {d[5]} "
                        f"\033[92mBusiness ID:\033[0m {d[6]} "
                        f"\033[92mBeneficiary ID:\033[0m {d[7]}"
                    )

                donation_id = input("\nEnter Donation ID to delete: ").strip()
                if not donation_id.isdigit():
                    print("\033[91m🚫 Donation ID must be numeric.\033[0m")
                    continue

                delete_entry("DELETE FROM Donation WHERE Donation_ID=?", donation_id)
                print("\033[92m🎉 Donation deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error deleting donation: {str(e)}\033[0m")

        # Option 5: Back to main menu
        elif choice == "5":
            break

if __name__ == "__main__":
    donation_menu()
