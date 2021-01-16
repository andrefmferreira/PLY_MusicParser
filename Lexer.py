# Lexer.py

import ply.lex as lex
import sys

class Lexer:
    # Documentation table
    # . --> note
    # ^ --> uo freq half
    # _ --> dn freq half
    # ^{12} up freq 12 half
    # > dn note velocity
    # < up note velocity
    # * pause
    # ~ join notes
    # : raises accord 3x up
    #  do re mi fa sol la si
    #   .^^.^^.^.^^.^^.^^.^^.
    #   c  d  e f  g  a  b
    # si la sol fa mi re do
    #  .__.__.__._.__.__.
    #  # ignore line

    t_ignore = " \n"
    literals = "=[]\\"
    tokens = ("NOTE", "UP", "DN", "VAL", "FASTER", "SLOWER", "PAUSE", "JOIN", "HIGHCHORD", "RUNMACRO", "MACRO")

    # note is defined by dot '.'
    def t_NOTE(self, t):
        r"""\.|[a-g]"""
        return t

    # ^ increases in half a tone the following note
    def t_UP(self, t):
        r"""\^+"""
        return t

    # ^ decreases in half a tone the following note
    def t_DN(self, t):
        r"""\_+"""
        return t

    # value for the factor of increase or decrease in the half-tone
    def t_VAL(self, t):
        r"""{[1-9][0-9]*}"""
        t.value = int(t.value[1:-1])
        return t

    # speeds up the following note
    def t_FASTER(self, t):
        r"""<+"""
        return t

    # slows down the following note
    def t_SLOWER(self, t):
        r""">+"""
        return t

    # pauses the tone
    def t_PAUSE(self, t):
        r"""\*+"""
        return t

    # joins 2 notes
    def t_JOIN(self, t):
        r"""\~"""
        return t

    # bigger chord
    def t_HIGHCHORD(self, t):
        r""":"""
        return t

    # ignores comments
    def t_IGNORE(self, t):
        r"""\#.*[\n]|[\n]|[ ]"""
        pass

    def t_RUNMACRO(self, t):
        r"""\\[A-Z]+"""
        return t


    def t_MACRO(self, t):
        r"""[A-Z]+="""
        return t


    # def t_MACRONOTES(self, t):
    #     r"""\[[\.a-g^_~*:]+\]"""
    #     return t



    # defines error for lexer
    def t_error(self, t):
        print(f"Parser error. Unexpected char: {t.value[0]}", file=sys.stderr)
        exit(1)


    # inits Lexer object
    def __init__(self):
        self.lexer = None

    # builds/starts the process
    def Build(self, input, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.input(input)
