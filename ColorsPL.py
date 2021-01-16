#colorsPL.py

#This file states color codes for output in console/terminal

# code learnt from: https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
# example:
# print(f"{bcolors.WARNING}Warning: No active frommets remain. Continue?{bcolors.RESET}")
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
