# Parser.py

from Lexer import Lexer
from Partiture import make_midi
import ply.yacc as yacc
import sys
from ColorsPL import bcolors
from Composer import Composer


class Parser:
    tokens = Lexer.tokens

    def __init__(self):
        self.parser = None
        self.lexer = None
        self.cNote = 60  # start values for notes
        self.cDur = 16  # start values for duration
        self.notes = []
        self.commands = []
        self.macros = {}

    def Parse(self, input, file, **kwargs):
        self.lexer = Lexer()
        self.lexer.Build(input, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)
        self.commands = self.parser.parse(lexer=self.lexer.lexer)
        # print(f"Comandos: {self.commands}\n")
        Composer.compose(self.commands, self)

        if make_midi(self.notes, file):
            print(
                f"{bcolors.OKGREEN}File {bcolors.OKCYAN}{file}.midi{bcolors.OKGREEN} generated successfully{bcolors.RESET}")
            print(f"{bcolors.WARNING}*************************************************{bcolors.RESET}\n")

        else:
            print(f"{bcolors.FAIL}File {bcolors.OKCYAN}{file}.midi{bcolors.FAIL} not generated{bcolors.RESET}", file=sys.stderr)
            print(f"{bcolors.WARNING}*************************************************{bcolors.RESET}\n", file=sys.stderr)

    # error for yacc
    def p_error(self, p):
        print("Syntax error", file=sys.stderr)
        if p:
            print(f"Unexpected token '{p.type}'", file=sys.stderr)
        exit(1)

    # first note // start of melody
    def p_music0(self, p):
        """  music  :   action  """
        p[0] = [p[1]]

    # following notes of melody
    def p_music1(self, p):
        """  music  :  music action  """
        lst = p[1]
        lst.append(p[2])
        p[0] = lst

    # sets the commands for a macro
    def p_action_def_macro(self, p):
        r""" action : MACRO '[' music ']' """
        p[0] = Composer('def_macro', {'name': p[1][:-1], 'notes': p[3]})

    # runs the stored commands in the macro
    def p_action_run_macro(self, p):
        """ action : RUNMACRO """
        p[0] = Composer('run_macro', {'name': p[1][1:]})

    # just the note
    def p_action0(self, p):
        """ action : NOTE """
        args = {'note': p[1]}
        p[0] = Composer('note', args)

    # takes an action that affects notes
    def p_action1(self, p):
        """ action : up
                   | dn
                   | faster
                   | slower """
        if '^' in p[1]:
            args = {'val': len(p[1])}
            p[0] = Composer('raise', args)
        elif '_' in p[1]:
            args = {'val': len(p[1])}
            p[0] = Composer('lower', args)
        elif '<' in p[1]:
            args = {'val': len(p[1]) * 2}
            p[0] = Composer('faster', args)
        elif '>' in p[1]:
            args = {'val': len(p[1]) * 2}
            p[0] = Composer('slower', args)

    # defines a pause
    def p_action2(self, p):
        """ action : PAUSE """
        args = {'val': len(p[1])}
        p[0] = Composer('pause', args)

    # defines a merge between notes
    def p_action3(self, p):
        """ action : NOTE JOIN NOTE
                   | NOTE JOIN faster NOTE
                   | NOTE JOIN slower NOTE """
        if len(p) == 4:
            if '<' in p[3]:
                args = {'val': len(p[3]),
                        'note': p[1]}
            else:
                args = {'val': -len(p[3]),
                        'note': p[1]}
        else:
            args = {'val': 1,
                    'note': p[1]}
        p[0] = Composer('merge', args)

    # sets an highchord
    def p_action4(self, p):
        """ action : highchord """
        p[0] = p[1]

    # raises half freq. by one
    def p_up0(self, p):
        """ up : UP """
        p[0] = p[1]

    # produces a '^' times a factor
    def p_up1(self, p):
        """ up : up val"""
        p[0] = p[1] * p[2]

    # lowers half freq. by one
    def p_dn0(self, p):
        """ dn : DN """
        p[0] = p[1]

    # produces a '_' times a factor
    def p_dn1(self, p):
        """ dn : dn val"""
        p[0] = p[1] * p[2]

    # gets the value factor
    def p_val(self, p):
        """ val : VAL """
        p[0] = p[1]

    # speeds up
    def p_faster0(self, p):
        """ faster : FASTER """
        p[0] = p[1]

    # slows down
    def p_slower0(self, p):
        """ slower : SLOWER """
        p[0] = p[1]

    # highchord command
    def p_highchord(self, p):
        """ highchord : HIGHCHORD """
        args = {'levels': [0, 4, 7]}
        p[0] = Composer('hchord', args)
