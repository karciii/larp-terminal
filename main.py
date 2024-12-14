from tr import BootSequence, tr
from animations import slow_print
from colorama import Fore

if __name__ == "__main__":
    try:     
        terminal = tr() 
        terminal.start()  

    except KeyboardInterrupt:
        slow_print("\nProgram zakończony.")
