#event.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
This module handles all event-related operations in the donation system.
It provides a menu interface for managing fundraising events including:
- Viewing all events
- Adding new events
- Updating existing events
- Deleting events (with dependency checks)
"""

from start.crud import view_all, add_entry, update_entry, delete_entry
import re

def event_menu():
    """
    Displays and manages the event management menu.
    Provides continuous interface for event operations until user exits.
    Handles all CRUD operations for event records with proper validation.
    """
    while True:
        # Display menu options with green header
        print("\n\033[92m--- Event Management ---\033[0m", flush=True)
        print("1. View All Events")
        print("2. Add Event")
        print("3. Update Event")
        print("4. Delete Event")
        print("5. Back to Main Menu")
        
        # Get and validate user choice
        choice = input("\033[92mChoose an option (1-5): \033[0m").strip()
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91mInvalid choice. Please choose a number between 1 and 5.\033[0m")
            continue

        # Option 1: View all events
        if choice == "1":
            try:
                print("\n\033[92mAll Events:\033[0m")
                events = view_all("Event")
                if not events:
                    print("\033[93mNo events found in database.\033[0m")
                else:
                    for event in events:
                        print(
                            f"\033[92mID:\033[0m {event[0]} "
                            f"\033[92mName:\033[0m {event[1]} "
                            f"\033[92mDate:\033[0m {event[2]} "
                            f"\033[92mLocation:\033[0m {event[3]} "
                            f"\033[92mGoal:\033[0m £{event[4]:,.2f} "
                            f"\033[92mDescription:\033[0m {event[5]}"
                        )
            except Exception as e:
                print(f"\033[91mError viewing events: {str(e)}\033[0m")

        # Option 2: Add new event
        elif choice == "2":
            try:
                print("\n\033[93mTip: Event name cannot be empty and should be clear.\033[0m")
                name = input("Event Name: ").strip()
                if not name:
                    print("\033[91mEvent name cannot be empty.\033[0m")
                    continue
                
                print("\033[93mTip: Use the format YYYY-MM-DD for date.\033[0m")
                date = input("Date (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("\033[91mDate must be in YYYY-MM-DD format.\033[0m")
                    continue
                
                print("\033[93mTip: Location cannot be left blank.\033[0m")
                location = input("Location: ").strip()
                if not location:
                    print("\033[91mLocation cannot be empty.\033[0m")
                    continue
                
                print("\033[93mTip: Goal must be a positive number (e.g., 5000.00).\033[0m")
                try:
                    goal = float(input("Fundraising Goal: £"))
                    if goal <= 0:
                        raise ValueError("Goal must be positive")
                except ValueError:
                    print("\033[91mInvalid amount. Please enter a positive number.\033[0m")
                    continue
                
                print("\033[93mTip: Goal must be a positive number (e.g., 5000.00).\033[0m")
                desc = input("Description: ").strip()

                add_entry(
                    "INSERT INTO Event VALUES (NULL,?,?,?,?,?)",
                    (name, date, location, goal, desc)
                )
                print("\033[92mEvent added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError adding event: {str(e)}\033[0m")

        # Option 3: Update event
        elif choice == "3":
            print("\n\033[92mList of All Events:\033[0m")
            for event in events:
                        print(
                            f"\033[92mID:\033[0m {event[0]} "
                            f"\033[92mName:\033[0m {event[1]} "
                            f"\033[92mDate:\033[0m {event[2]} "
                            f"\033[92mLocation:\033[0m {event[3]} "
                            f"\033[92mGoal:\033[0m £{event[4]:,.2f} "
                            f"\033[92mDescription:\033[0m {event[5]}"
                        )
            try:
                print("\n\033[93mTip: Enter the ID of the event you'd like to update.\033[0m")
                event_id = input("Enter Event ID to update: ").strip()
                if not event_id.isdigit():
                    print("\033[91mEvent ID must be a number.\033[0m")
                    continue
                
                print("\033[93mTip: Event name cannot be empty.\033[0m")
                name = input("New Name: ").strip()
                if not name:
                    print("\033[91mEvent name cannot be empty.\033[0m")
                    continue
                
                print("\033[93mTip: Use the format YYYY-MM-DD for date.\033[0m")
                date = input("New Date (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("\033[91mDate must be in YYYY-MM-DD format.\033[0m")
                    continue
                
                print("\033[93mTip: Use the format YYYY-MM-DD for date.\033[0m")
                location = input("New Location: ").strip()
                if not location:
                    print("\033[91mLocation cannot be empty.\033[0m")
                    continue
                
                print("\033[93mTip: Goal must be a positive number.\033[0m")
                try:
                    goal = float(input("New Fundraising Goal: £"))
                    if goal <= 0:
                        raise ValueError("Goal must be positive")
                except ValueError:
                    print("\033[91mInvalid amount. Please enter a positive number.\033[0m")
                    continue

                desc = input("New Description: ").strip()

                print("\033[93mTip: Description is optional but recommended.\033[0m")
                update_entry(
                    "UPDATE Event SET Name=?, Date=?, Location=?, Fundraising_Goal=?, Description=? WHERE Event_ID=?",
                    (name, date, location, goal, desc, event_id)
                )
                print("\033[92mEvent updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91mError updating event: {str(e)}\033[0m")

        # Option 4: Delete event (with dependency checks)
        elif choice == "4":
            try:
                print("\n\033[92mList of All Events:\033[0m")
                for event in view_all("Event"):
                    print(
                        f"\033[92mID:\033[0m {event[0]} "
                        f"\033[92mName:\033[0m {event[1]} "
                        f"\033[92mDate:\033[0m {event[2]} "
                        f"\033[92mLocation:\033[0m {event[3]} "
                        f"\033[92mGoal:\033[0m £{event[4]:,.2f} "
                        f"\033[92mDescription:\033[0m {event[5]}"
                    )

                print("\n\033[93mTip: Please enter the ID number of the event you wish to delete.\033[0m")
                print("\033[93mTip: Deleting an event will also remove all linked donations and volunteers.\033[0m\n")

                event_id = input("Enter Event ID to delete: ").strip()
                if not event_id.isdigit():
                    print("\033[91mEvent ID must be a number.\033[0m")
                    continue

                delete_entry("DELETE FROM Event WHERE Event_ID=?", event_id)
                print("\033[92mEvent and all related donations and volunteers deleted successfully.\033[0m")

            except Exception as e:
                print(f"\033[91mError deleting event: {str(e)}\033[0m")


        # Option 5: Exit to main menu
        elif choice == "5":
            break

if __name__ == "__main__":
    event_menu()
