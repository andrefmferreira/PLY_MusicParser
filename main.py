# main.py
from ColorsPL import bcolors
from Parser import Parser
import sys
import os


print(f"{bcolors.WARNING} *********************************************** ")
print(f"{bcolors.WARNING}***         {bcolors.HEADER}Welcome to PL midi parser!{bcolors.WARNING}        ***")
print(f"{bcolors.WARNING} *********************************************** {bcolors.RESET}\n")

# check if file/directory is passed as parameter in main call
if len(sys.argv) == 1:
    print(f"{bcolors.WARNING}!! No file or folder passed as parameter{bcolors.RESET}")
    param = input(f"{bcolors.OKCYAN}>> Please indicate a file or folder: {bcolors.RESET}")
    print("")  # just to enter a paragraph
else:
    param = sys.argv[1]

files = []  # empty list of files

# check if parameter is a file or folder
if os.path.isfile(param):
    files.append(param)
elif os.path.isdir(param):
    files = next(os.walk(param))[2]
    files.reverse()  # just to put some order
else:
    print(f"{bcolors.WARNING}!! No valid file or folder were given !!{bcolors.RESET}", file=sys.stderr)
    print(f"{bcolors.FAIL}   Exiting program ...{bcolors.RESET}", file=sys.stderr)
    exit(1)

# runs all files
for file in files:
    if len(files) > 1:
        file = param + file

    # open file(s) in read mode
    with open(file, mode="r") as f:
        musicalNotes = f.read()
    musicParser = Parser()

    file = file.split("/")

    # sets the "filename" to use it in the output
    print(f"{bcolors.WARNING}Processing file: {bcolors.OKCYAN}{bcolors.BOLD}{file[len(file)-1]}{bcolors.RESET}")
    file = file[len(file)-1].split(".")
    file = file[0]

    # starts the parsing
    musicParser.Parse(musicalNotes, file)
