# Partiture.py


# this outputs the  parsed notes, to a midi file, saving it with same name as the input file, with midi extension.
from mxm.midifile import MidiOutFile


def make_midi(melody, file):
    out_file = open(f"./output/{file}.midi", 'wb')
    midi = MidiOutFile(out_file)
    midi.header(format=0, nTracks=1, division=32)
    midi.start_of_track()

    # print(f"Midi_notes: {melody}")

    try:
        for note, duration in melody:
            if note is 0:       # if it is a pause
                midi.note_on(channel=0, note=0)
                midi.update_time(0)
                midi.note_off(channel=0, note=0)
                midi.update_time(duration)
                midi.note_on(channel=0, note=0)
                midi.update_time(0)
                midi.note_off(channel=0, note=0)
                midi.update_time(0)
            else:
                midi.update_time(0)
                if isinstance(note, list):  # checks if note is single, or chord
                    for n in note:
                        midi.note_on(channel=0, note=n)
                else:
                    midi.note_on(channel=0, note=note)
                midi.update_time(duration)
                if isinstance(note, list):
                    for n in note:
                        midi.note_off(channel=0, note=n)
                else:
                    # if note is not 0:
                    midi.note_off(channel=0, note=note)
        midi.update_time(0)
        midi.end_of_track()
    except:
        return False
    return True
