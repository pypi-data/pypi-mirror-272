from colorama import init, Fore, Style
from datetime import datetime

init()

class ParPrint:
    SUCCESS = Fore.GREEN
    FAILED = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.BLUE
    CYAN = Fore.CYAN
    END = Style.RESET_ALL

    @staticmethod
    def _get_current_time():
        return datetime.now().strftime("[%H:%M:%S]")

    def __init__(self, text, status, time=False):
        if time:
            time_prefix = f"{self.CYAN}{self._get_current_time()}{self.END} "
        else:
            time_prefix = ""
            
        if status == "Success":
            print(f"{time_prefix}{self.SUCCESS}{text}{self.END}")
        elif status == "Failed":
            print(f"{time_prefix}{self.FAILED}{text}{self.END}")
        elif status == "Warning":
            print(f"{time_prefix}{self.WARNING}{text}{self.END}")
        elif status == "Info":
            print(f"{time_prefix}{self.INFO}{text}{self.END}")
        else:
            print(f"{time_prefix}{text}")

# Example usage
if __name__ == "__main__":
    ParPrint("This is a test", "Success", time=True)
    ParPrint("This is a test", "Failed", time=True)
    ParPrint("This is a test", "Warning", time=True)
    ParPrint("This is a test", "Normal", time=True)