import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

NOTE_NAMES  = np.array(["A", "A#", "Bb", "B", "C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab"])
NOTE_POS    = np.array([0  ,    1,    1,   2,   3,    4,    4,   5,    6,    6,   7,   8,    9,    9,  10,   11,   11])
SCALES = {
    "heptatonic":dict(
        major=[2, 2, 1, 2, 2, 2, 1],
        minor=[2, 1, 2, 2, 1, 2, 2]
    ),
    "12": dict(
        natural=[1,1,1,1,1,1,1,1,1,1,1,1]
    )
}


def note2num(note_names):

    result = []
    if np.asarray(note_names).size == 1:
        note_names = [note_names]
    
    for note_name in np.asarray(note_names):

        note_id = np.ravel(np.argwhere(NOTE_NAMES == note_name))

        if note_id.size == 1:
            note_id = note_id[0]

        note_id = NOTE_POS[note_id]

        result.append(note_id)

    if len(result) == 1:
        return result[0]
    else:
        return np.array(result)


def num2note(note_positions, accidental="#"):
    "For the accidental keyword choose among '#', 'b', or 'both'."

    result = []
    if np.asarray(note_positions).size == 1:
        note_positions = [note_positions]

    for note_position in np.asarray(note_positions):

        note_id = np.ravel(np.argwhere(NOTE_POS == note_position))

        if note_id.size == 1:
            note_id = note_id[0]
        elif note_id.size > 1:

            if accidental == "#":
                note_id = note_id[0] # only select the note designation with a specific type of accidental (in this case: #)
            elif accidental == "b":
                note_id = note_id[1]

        note_id = NOTE_NAMES[note_id]



        result.append(note_id)

    if len(result) == 1:
        return result[0]
    else:
        if accidental == "both":
            return result
        else:
            return np.array(result)



class Scale():

    def __init__(self, root_note, intervals):
        
        self.root_note_name = root_note
        self.root_note = note2num(root_note)
        self.intervals = intervals
        self.Nintervals = len(intervals)
        try:
            self.type = {
                5: "pentatonic",
                6: "hexatonic",
                7: "heptatonic",
                8: "octatonic"
            }[len(intervals)]
        except KeyError:
            self.type = str(len(intervals))
    

    def get_interval(self, interval:int, numeric=False):

        if interval == 1:
            return {
                False: self.root_note_name,
                True:  self.root_note
            }[numeric]
        
        result = self.root_note
        for i in range(interval - 1):
            result += self.intervals[i % self.Nintervals]
        
        return {
            False: num2note(result),
            True:  result
        }[numeric]




class Keyboard():

    def __init__(self, Nkeys, key0, key_ratio = 5.):

        self.key0 = key0
        self.Nkeys = Nkeys

        fig = plt.figure(figsize=(3./key_ratio, 3.))
        keyboard = fig.add_axes([0, 0, 1, 0.8])
        keyboard.axis("off")

        self.keys = []
        self.labels = []
        self.keytype = []
        x_position = 0

        # generate the keys and labels
        for i in np.arange(Nkeys):
            if (i + key0) % 12 in [0, 2, 3, 5, 7, 8, 10]: # white key
                new_key = keyboard.add_patch(mpl.patches.FancyBboxPatch(
                    [x_position, 0], 1., key_ratio, fc="white", ec="black", boxstyle="round, pad=0., rounding_size=0.1"
                ))
                self.keytype.append("w")
                new_label = keyboard.text(x_position + 0.5, -0.1, num2note((i + key0) % 12), zorder=10, transform=keyboard.transData, fontsize=10, ha="center", va="top")


                x_position += 1




            else: # black key
                new_key = keyboard.add_patch(mpl.patches.FancyBboxPatch(
                    [x_position-1./3., 2], 2./3., key_ratio - 2., fc="black", zorder=2, boxstyle="round, pad=0., rounding_size=0.1"
                ))
                self.keytype.append("b")
                new_label = keyboard.text(x_position, key_ratio + 0.1, "%s\n%s" % tuple(num2note((i + key0) % 12, accidental="both")), zorder=10, transform=keyboard.transData, fontsize=10, ha="center", va="bottom")

            self.keys.append(new_key)
            self.labels.append(new_label)

        del x_position

        self.fig      = fig
        self.keyboard = keyboard
    

    def press_key(self, keynums, pressed_white_key_color="#ff9900", pressed_black_key_color="#aa6600"):

        if np.asarray(keynums).size == 1:
            keynums = np.ravel([keynums])

        for keynum in np.asarray(keynums):
            if self.keytype[keynum] == "b":
                self.keys[keynum].set_facecolor(pressed_black_key_color)
                self.labels[keynum].set_color(pressed_black_key_color)
            else:
                self.keys[keynum].set_facecolor(pressed_white_key_color)
                self.labels[keynum].set_color(pressed_white_key_color)


    def get_keys_from_scale(self, scale, root_note, scale_type="heptatonic"):
        
        root_note = np.ravel(np.argwhere(NOTE_NAMES == root_note))[0]
        root_note = NOTE_POS[root_note]

        key_to_add = root_note - 12 # start an octave lower that nthe root note
        result = []
        iterator = 0
        while key_to_add < self.Nkeys:

            if key_to_add >= 0:
                result.append(key_to_add)

            key_to_add += SCALES[scale_type][scale][iterator % len(SCALES[scale_type][scale])]

            iterator += 1

        return result





if __name__ == "__main__":

    main_key = ("major", "C")
    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages("output.pdf") as pdf:

        for current_chord in [
            ("major", "C"),
            ("major", "F"),
            ("minor", "A"),
            ("minor", "E"),
            ("major", "G"),
            ("major", "D")
        ]:
            kb = Keyboard(88, 0)
            kb.keyboard.set_ylim(0, 5)
            kb.keyboard.set_xlim(0, 52)
            kb.fig.set_figwidth(16)
            kb.fig.suptitle("%s%s and %s%s" % (current_chord[1], current_chord[0], main_key[1], main_key[0]))

            # find all keys for a given scale
            scale1 = kb.get_keys_from_scale(*main_key)
            scale2 = kb.get_keys_from_scale(*current_chord)
            kb.press_key(np.intersect1d(scale1, scale2), pressed_white_key_color=mpl.colormaps["viridis"](.5), pressed_black_key_color=mpl.colormaps["viridis"](.25))
            
            # find all root keys, thirds, fifths and sevenths
            scale1 = Scale(root_note=main_key[1], intervals=SCALES["heptatonic"][main_key[0]])
            scale2 = Scale(root_note=current_chord[1], intervals=SCALES["heptatonic"][current_chord[0]])
            
            thirds_fifths = np.union1d([scale1.get_interval(interval, numeric=True) for interval in [3, 5]], [scale2.get_interval(interval, numeric=True) for interval in [3, 5]]) % 12
            roots         = np.union1d([scale1.get_interval(1, numeric=True)], [scale2.get_interval(1, numeric=True)]) % 12
            sevenths      = np.union1d([scale1.get_interval(7, numeric=True)], [scale2.get_interval(7, numeric=True)]) % 12

            for key in np.arange(kb.Nkeys):

                if key % 12 in sevenths:
                    kb.press_key(key, pressed_white_key_color="#888888", pressed_black_key_color="#555555")

                if key % 12 in thirds_fifths:
                    kb.press_key(key, pressed_white_key_color=mpl.colormaps["twilight_shifted"](.75), pressed_black_key_color=mpl.colormaps["twilight_shifted"](.25))
            
                if key % 12 in roots:
                    kb.press_key(key, pressed_white_key_color="#f5bf42", pressed_black_key_color="#755c21")

            pdf.savefig(kb.fig, bbox_inches="tight")
            plt.close()