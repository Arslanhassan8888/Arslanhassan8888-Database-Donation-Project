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
from body.business import business_menu
from body.beneficiary import beneficiary_menu
from body.donation import donation_menu
from body.search import search_menu
from body.volunteer import volunteer_menu  

def main_menu():
    # Initialize database with tables and sample data
    create_tables()        # Creates all required database tables with ON DELETE CASCADE enabled
    insert_sample_data()   # Populates with initial sample records

    while True:
        # Display main application header and options
        
        print("\n\033[92m/ WELCOME TO ARSLAN'S DONATION MANAGEMENT SYSTEM  /\033[0m")
        print("\n" + "-" * 60)
        print("🏠  Main Menu:")
        print("-" * 60)
        print("1️⃣  Donor Management")
        print("2️⃣  Event Management")
        print("3️⃣  Business Management")
        print("4️⃣  Beneficiary Management")
        print("5️⃣  Donation Management")
        print("6️⃣  Volunteer Management") 
        print("7️⃣  🔍 Search Records")
        print("8️⃣  🚪 Exit")
        print("-" * 60)

        # Get user's menu choice
        choice = input("\n Enter your choice (1-8): ").strip()

        # Validate input is a number between 1-8
        if not choice.isdigit() or choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("\n🚫 Invalid choice. Please enter a number between 1 and 8.\n")
            continue

        # Route to the appropriate module based on user choice
        match choice:
            case "1":
                donor_menu()
            case "2":
                event_menu()
            case "3":
                business_menu()
            case "4":
                beneficiary_menu()
            case "5":
                donation_menu()
            case "6":
                volunteer_menu()  
            case "7":
                search_menu()
            case "8":
                print("\033[92m🎉 THANK YOU for using Arslan's Donation App! Goodbye! 🎉\033[0m")
                break

# Allow running this module directly
if __name__ == "__main__":
    main_menu()
