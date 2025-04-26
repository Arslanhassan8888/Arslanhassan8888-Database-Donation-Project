# event.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""
This module handles all event-related operations in the donation system.
It provides a menu interface for managing fundraising events including:
- Viewing all events
- Adding new events
- Updating existing events
- Deleting events (with donation checks)
"""

from start.crud import view_all, add_entry, update_entry, delete_entry, linked_donations
import re
def event_menu():
    """
    Displays and manages the event management menu.
    Provides continuous interface for event operations until user exits.
    Handles all CRUD operations for event records with proper validation.
    """
    while True:
        # Print menu options with decoration
        print("\n" + "🎯  EVENT MANAGEMENT MENU  🎯".center(60))
        print("\n" + "-" * 60)
        print("1️⃣  View All Events")
        print("2️⃣  Add Event")
        print("3️⃣  Update Event")
        print("4️⃣  Delete Event")
        print("5️⃣  🔙 Back to Main Menu")
        print("-" * 60)

        choice = input("\n Choose an option (1-5): ").strip()

        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5"]:
            print("\033[91m🚫 Invalid choice. Please choose a number between 1 and 5.\033[0m")
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
                print(f"\033[91m🚫 Error viewing events: {str(e)}\033[0m")

        # Option 2: Add new event
        elif choice == "2":
            try:
                print("\n\033[93mTip: Event name cannot be empty and should be clear.\033[0m")
                name = input("Event Name: ").strip()
                if not name:
                    print("\033[91m🚫 Event name cannot be empty.\033[0m")
                    continue

                print("\033[93mTip: Use the format YYYY-MM-DD for date.\033[0m") 
                date = input("Date (YYYY-MM-DD): ").strip() 
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date): # Validate date format Check if date is in YYYY-MM-DD format using regex
                    print("\033[91m🚫 Date must be in YYYY-MM-DD format.\033[0m")
                    continue

                print("\033[93mTip: Location cannot be left blank.\033[0m")
                location = input("Location: ").strip()
                if not location:
                    print("\033[91m🚫 Location cannot be empty.\033[0m")
                    continue

                print("\033[93mTip: Goal must be a positive number (e.g., 5000.00).\033[0m") 
                try:
                    goal = float(input("Fundraising Goal: £")) #Check if goal is a positive number 
                    if goal <= 0: 
                        raise ValueError("Goal must be positive") 
                except ValueError:
                    print("\033[91m🚫 Invalid amount. Please enter a positive number.\033[0m")
                    continue

                desc = input("Description (optional): ").strip()

                add_entry(
                    "INSERT INTO Event VALUES (NULL,?,?,?,?,?)",
                    (name, date, location, goal, desc)
                )
                print("\033[92m🎉 Event added successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error adding event: {str(e)}\033[0m")

        # Option 3: Update event
        elif choice == "3":
            print("\n\033[92mList of All Events:\033[0m")
            events = view_all("Event")
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
                print("\n\033[93mTip: Enter the ID of the event you want to update.\033[0m")
                event_id = input("Enter Event ID to update: ").strip()
                if not event_id.isdigit():
                    print("\033[91m🚫 Event ID must be a number.\033[0m")
                    continue

                name = input("New Event Name: ").strip()
                if not name:
                    print("\033[91m🚫 Event name cannot be empty.\033[0m")
                    continue

                date = input("New Date (YYYY-MM-DD): ").strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                    print("\033[91m🚫 Date must be in YYYY-MM-DD format.\033[0m")
                    continue

                location = input("New Location: ").strip()
                if not location:
                    print("\033[91m🚫 Location cannot be empty.\033[0m")
                    continue

                try:
                    goal = float(input("New Fundraising Goal: £"))
                    if goal <= 0:
                        raise ValueError("Goal must be positive")
                except ValueError:
                    print("\033[91m🚫 Invalid amount. Please enter a positive number.\033[0m")
                    continue

                desc = input("New Description (optional): ").strip()

                update_entry(
                    "UPDATE Event SET Name=?, Date=?, Location=?, Fundraising_Goal=?, Description=? WHERE Event_ID=?",
                    (name, date, location, goal, desc, event_id)
                )
                print("\033[92m🎉 Event updated successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error updating event: {str(e)}\033[0m")

        # Option 4: Delete event
        elif choice == "4":
            print("\n\033[92mList of All Events:\033[0m")
            events = view_all("Event")
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
                print("\n\033[93mTip: Enter the ID of the event you want to delete.\033[0m")
                event_id = input("Enter Event ID to delete: ").strip()
                if not event_id.isdigit():
                    print("\033[91m🚫 Event ID must be a number.\033[0m")
                    continue

                if linked_donations("Event_ID", event_id):
                    print("\033[91m🚫 Cannot delete Event linked to existing Donations.\033[0m")
                    continue

                delete_entry("DELETE FROM Event WHERE Event_ID=?", event_id)
                print("\033[92m🎉 Event deleted successfully.\033[0m")
            except Exception as e:
                print(f"\033[91m🚫 Error deleting event: {str(e)}\033[0m")

        elif choice == "5":
            break

if __name__ == "__main__":
    event_menu()
