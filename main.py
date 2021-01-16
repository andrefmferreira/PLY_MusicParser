# main.py
from ColorsPL import bcolors
from Parser import Parser
import sys

# . representa uma nota
# ^ representa a subida da frequencia em meio tom
# _ representa a descida da frequencia em meio tom
# ^{12} representa a subida de 12 meios tons
# > ou < diminui ou aumenta a velocidade das notas
# se tiver # deve ser ignorada
#   * pausa
# ~ junção de notas
#  : reproduz um acord 3x acima
#  do re mi fa sol la si
#   .^^.^^.^.^^.^^.^^.^^.       aumenta meio tom cada ^
#
# si la sol fa mi re do         diminui meio tom cada _
# .__.__.__._.__.__.

print(f"{bcolors.WARNING}****************************************{bcolors.RESET}")
print(f"{bcolors.WARNING}**     {bcolors.HEADER}Welcome to PL midi parser!{bcolors.WARNING}     **{bcolors.RESET}")
print(f"{bcolors.WARNING}****************************************{bcolors.RESET}\n")


if len(sys.argv) == 1:
    print(f"{bcolors.WARNING}No file passed as parameter{bcolors.RESET}")
    file = input(f"{bcolors.OKCYAN}>> Please indicate the file: {bcolors.RESET}")
else:
    file = sys.argv[1]
# file = './input/exemplomacro2.in'
with open(file, mode="r") as f:
    musicalNotes = f.read()
musicParser = Parser()

file = file.split("/")

print(f"{bcolors.WARNING}Selected file: {bcolors.OKCYAN}{bcolors.BOLD}{file[len(file)-1]}{bcolors.RESET}")
file = file[len(file)-1].split(".")
file = file[0]

musicParser.Parse(musicalNotes, file)
