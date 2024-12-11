from tr import BootSequence, tr
from animations import slow_print
from colorama import Fore

if __name__ == "__main__":
    try:
        boot_instance = BootSequence()
        boot_instance.run()  
        
        terminal = tr() 
        terminal.start()  

    except KeyboardInterrupt:
        slow_print("\nProgram zakończony.")
