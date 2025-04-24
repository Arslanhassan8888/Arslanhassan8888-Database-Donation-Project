# main.py
"""
This is the entry point of the Donation Management System application.
It serves as the launchpad that starts the entire program by calling the main menu.
The file is kept minimal intentionally - all application logic resides in other modules.

"""
from initialize.menu import main_menu

if __name__ == "__main__":
    main_menu()