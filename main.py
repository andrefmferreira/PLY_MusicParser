# main.py
from ColorsPL import bcolors
from Parser import Parser
import sys


print(f"{bcolors.WARNING}****************************************{bcolors.RESET}")
print(f"{bcolors.WARNING}**     {bcolors.HEADER}Welcome to PL midi parser!{bcolors.WARNING}     **{bcolors.RESET}")
print(f"{bcolors.WARNING}****************************************{bcolors.RESET}\n")

# check if file is passed as parameter in main call
if len(sys.argv) == 1:
    print(f"{bcolors.WARNING}No file passed as parameter{bcolors.RESET}")
    file = input(f"{bcolors.OKCYAN}>> Please indicate the file: {bcolors.RESET}")
else:
    file = sys.argv[1]

# open file in read mode
with open(file, mode="r") as f:
    musicalNotes = f.read()
musicParser = Parser()

file = file.split("/")

# sets the "filename" to use it in the output
print(f"{bcolors.WARNING}Selected file: {bcolors.OKCYAN}{bcolors.BOLD}{file[len(file)-1]}{bcolors.RESET}")
file = file[len(file)-1].split(".")
file = file[0]

# starts the parsing
musicParser.Parse(musicalNotes, file)
