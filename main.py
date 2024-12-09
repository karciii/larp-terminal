from encyclopedia import Encyclopedia
from journal import Journal
from tr import tr, trCommands
from animations import frame_effect, slow_print
from colorama import Fore


if __name__ == "__main__":
    try:
        tr = tr()
        tr.start()
        main_menu()
    except KeyboardInterrupt:
        slow_print("\nProgram terminated.")
