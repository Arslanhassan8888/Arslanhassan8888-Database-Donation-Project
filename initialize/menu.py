# menu.py
"""
This is the main entry point for the Donation Management System.
It provides the top-level menu that connects all system components.
The menu coordinates between different management modules and handles
the initial database setup.
"""

from start.tables import create_tables
from start.values import insert_sample_data
from body.donor import donor_menu
from body.event import event_menu
from body.business import volunteer_menu
from body.beneficiary import beneficiary_menu
from body.donation import donation_menu
from body.search import search_menu

def main_menu():
    # Initialize database with tables and sample data
    create_tables()        # Creates all required database tables with ON DELETE CASCADE enabled
    insert_sample_data()   # Populates with initial sample records

    while True:
        # Display main application header and options
        print("\n\033[92m===== Welcome to Arslan's Donation App =====\033[0m")
        print("Select your role:")
        print("1. Donor Management")
        print("2. Event Management")
        print("3. Donation Management")
        print("4. Volunteer Management")
        print("5. Beneficiary Management")
        print("6. Search Records")
        print("7. Exit")

        # Get user's menu choice
        choice = input("\033[92mEnter your choice (1-7): \033[0m").strip()

        # Validate input is a number between 1-7
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("\033[91mInvalid choice. Please enter a number between 1 and 7.\033[0m")
            continue

        # Route to the appropriate module based on user choice
        match choice:
            case "1": 
                donor_menu()       
            case "2": 
                event_menu()       
            case "3": 
                donation_menu()    
            case "4": 
                volunteer_menu()  
            case "5": 
                beneficiary_menu() 
            case "6": 
                search_menu()      
            case "7":
                print("\033[92mThank you for using Arslan's Donation App. Goodbye!\033[0m")
                break

# Allow running this module directly
if __name__ == "__main__":
    main_menu()
