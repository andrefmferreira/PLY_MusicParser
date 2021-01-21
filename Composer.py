# Composer.py

from AllNotes import letterNotes


# breve > minima > semi-minima < colcheia < semi-colcheia
#   64      32         16            8            4

# gets the tone
def whichTone(parser):
    for pianoKey in letterNotes:
        if parser.cNote == pianoKey[2]:
            return pianoKey[0]  # tone


# converts a letter note into a midi pitch value
def convertNote(note, parser):
    curTone = whichTone(parser)

    for pianoKey in letterNotes:
        if note == pianoKey[1] and curTone == pianoKey[0]:
            return pianoKey[2]


# sets the note
def do_note(action, parser):
    n = action.args['note']

    # checks if note needs conversion or not
    if n is not '.':
        parser.cNote = convertNote(n, parser)
    note = parser.cNote
    duration = parser.cDur

    if len(parser.notes) == 0:
        parser.notes = [[note, duration]]
    else:
        parser.notes.append([note, duration])


# function to raise note.
def do_raise(action, parser):
    val = action.args['val']
    parser.cNote = parser.cNote + val


# function to lower note.
def do_lower(action, parser):
    val = action.args['val']
    parser.cNote = parser.cNote - val


# function to speedup note.
def do_faster(action, parser):
    val = action.args['val']
    parser.cDur = parser.cDur * val


# function to slowdown note.
def do_slower(action, parser):
    val = action.args['val']
    parser.cDur = int(parser.cDur / val)  # cast to int mandatory for mxm.midi


# function to set the highchord
def do_hchord(action, parser):
    notes = []  # creates an empty list of notes
    for val in action.args['levels']:
        notes.append(parser.cNote + val)
    parser.notes.append([notes, parser.cDur])


# function to set a pause
def do_pause(action, parser):
    duration = parser.cDur * action.args['val']
    parser.notes.append([0, duration])


# function to merge notes
def do_merge(action, parser):
    val = action.args['val']
    duration = parser.cDur + int(val * parser.cDur)
    if duration < 0:  # checks if duration is less than 0. if so, 0 is the limit
        duration = 0
    parser.notes.append([parser.cNote, duration])


# defines a macro, and save its actions to a dictionary
def do_def_macro(action, parser):
    macro_name = action.args['name']
    macro_notes = action.args['notes']
    parser.macros[macro_name] = {'notes': macro_notes}


# Runs the macro, called by name. It access the macro dictionary, and runs the stored commands
def do_run_macro(action, parser):
    macro_name = action.args['name']

    if macro_name not in parser.macros:
        print(f"Unknown macro '{macro_name}'")
        exit(1)
    # saves the note and duration before the macro to restore them after it runs
    saveNote = parser.cNote
    saveDur = parser.cDur
    macro_partiture = parser.macros[macro_name]['notes']
    Composer.compose(macro_partiture, parser)
    parser.cNote = saveNote
    parser.cDur = saveDur

class Composer:
    dispatch_table = {
        'note': do_note,
        "pause": do_pause,
        "slower": do_slower,
        "faster": do_faster,
        'raise': do_raise,
        "lower": do_lower,
        "merge": do_merge,
        "hchord": do_hchord,
        "def_macro": do_def_macro,
        "run_macro": do_run_macro,
    }

    # constructor of Composer class
    def __init__(self, action, args):
        self.name = action
        self.args = args

    def __repr__(self):
        return f"Composer({self.name}, {self.args})"

    # executes functions based on dispatch_table calls
    def make(self, parser):
        self.dispatch_table[self.name](self, parser)

    @classmethod
    def compose(cls, partiture, parser):
        for notes in partiture:
            notes.make(parser)  # calls dispatch_table functions
