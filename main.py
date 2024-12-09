from encyclopedia import Encyclopedia
from journal import Journal
from tr import tr, trCommands
from animations import frame_effect, slow_print
from colorama import Fore

def main_menu():
    """Displays the main menu."""
    encyclopedia = Encyclopedia()
    journal = Journal()

    while True:
        frame_effect(" Main Menu ", width=60)
        slow_print(" 1. Open Encyclopedia ")
        slow_print(" 2. Open Journal ")
        slow_print(" 3. Scan Area ")
        slow_print(" 4. Hack System ")
        slow_print(" 5. Help ")
        slow_print(" 6. Exit ")
        choice = input(Fore.GREEN + "> ").strip()

        if choice == "1":
            encyclopedia.menu()
        elif choice == "2":
            journal_menu(journal)
        elif choice == "3":
            trCommands.gadget_scan()
        elif choice == "4":
            trCommands.gadget_hack()
        elif choice == "5":
            show_help()
        elif choice == "6":
            slow_print(Fore.YELLOW + "Exiting the program...")
            break
        else:
            slow_print(Fore.RED + "Invalid choice. Please try again.")

def show_help():
    """Displays help information."""
    help_text = """
    +------------------------------------------------------------+
    |                          Help                              |
    +------------------------------------------------------------+
    | 1. Open Encyclopedia - Access the in-game encyclopedia.    |
    | 2. Open Journal - Access and manage your journal entries.  |
    | 3. Scan Area - Perform a scan of the surrounding area.     |
    | 4. Hack System - Attempt to hack into a system.            |
    | 5. Help - Display this help information.                   |
    | 6. Exit - Exit the program.                                |
    +------------------------------------------------------------+
    """
    slow_print(Fore.CYAN + help_text)



if __name__ == "__main__":
    try:
        tr = tr()
        tr.start()
        main_menu()
    except KeyboardInterrupt:
        slow_print("\nProgram terminated.")
