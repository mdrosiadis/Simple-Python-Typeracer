#!/usr/bin/env python3
import tkinter as tk
import time

# oi metavlhtes poy xreiazetai to programma

# to keimeno pou prepei na grapsei o xrhsths
text = ""
# thesi epomenou xarakthra pou prepei na plhktrologhsoume
current_index = 0
# xronos pou paththike o prwtos xarakthras
start_time =  0
# flag gia to ama prepei na stamathsei to xronometro
timer_stop = False

# anoigoume to arxeio keimenou kai diabazoume ta periexomena tou
# afto to keimeno einai auto pou tha prepei na grapsei o xrhsths
with open('text.txt', 'r') as f:
    text = f.read().strip()

def timer_tick():
    """
    Synatrhsh poy kaloume mesw ths after() ths tkinter.
    Metraei to xrono apo thn enarxh tou paixnidiou, ypologizei WPM kai
    allazei to keimeno ths time_label
    """
    global timer_stop

    # ypologismos xronou apo thn stigmh pou arxise h plhktrologhsh
    end_time = time.time()
    current_time = end_time - start_time

    # poses lexeis exoume grapsei hdh
    words = len(text[:current_index].split(' '))

    # ypologismos lexewn ana lepto (wpm)
    time_in_minutes = current_time / 60
    wpm = words / time_in_minutes

    # grafoume to trexon wpm sto label
    text_to_label = "WPM: {:3d} ({:4d} words @ {:5.2f} sec!)".format(int(wpm), words, current_time)
    time_label.config(text=text_to_label)

    # dont let tkinter call tick again if the timer has been stopped
    if timer_stop:
        return

    # zhtame apo th tkinter na kalesei ksana afth th synarthsh meta apo 0.05 deuterolepta
    # gia na ananewsei to xronometro
    window.after(50, timer_tick)

def on_entry_key(key):
    """
    Synarthsh pou kaleitai kathe fora poy ena koumpi patietai sto entry.
    Elegxei an o xarathras einai swstos.

    @param key: to event pou kalese th synarthsh (unused)
    """
    global current_index, start_time, timer_stop

    # pairnoume to keimeno apo to type_entry
    entry_text = type_entry.get()

    # ksekiname to xronometro sto prwto xarakthra
    if current_index == 0:
        start_time = time.time()
        timer_tick()

    # protect against no text
    if not entry_text:
        return

    # an o xarakthras pou pathse o xrhsths einai o xarakthras pou perimenoume
    # kathws kai ana h lexh pou exei grapsei tairgiazei me afth pou perimenoume,
    # tote o xarakhtras pou paththike einai swstos.
    if entry_text[-1] == text[current_index] and text[:current_index].endswith(entry_text[:-1]):

        # Proxorame th thesi tou xarakthra pou perimenoume mia thesh mprosta
        current_index += 1

        # zwgrafizoume me prasino xrwma to meros tou keimenou poy exoume grapsei swsta mexri twra
        # dhladh apo tn arxh ("1.0") mexri kai osous xarakhtres exoume grapsei swsta mexri twra (current_index)
        text_widget.tag_add("correct", "1.0", f"1.0+{current_index}c")

        # grapsame olo to keimeno
        if current_index == len(text):
            # blockaroume to entry gia na mhn mporoume na plhktrologhsoume allo
            type_entry.delete(0, 'end')
            type_entry.config(state=tk.DISABLED)

            # stamatame to xronometro
            timer_stop = True

        # an eimaste se telos lexhs, katharise to entry
        if entry_text[-1] == ' ':
            type_entry.delete(0, 'end')


# kataskevh basikou parathirou, orismos megethous kai titlou
window = tk.Tk()
window.geometry("500x500")
window.wm_title("Type Racer!")

# To Text widget tha periexei to keimeno pou prepei na grapsei o paikths
text_widget = tk.Text(window, bg="#add8e6")
text_widget.insert('1.0', text)
text_widget.config(state=tk.DISABLED)
text_widget.tag_configure("correct", foreground="green")
text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Se afto to Label widget tha grafoume to xrono kathos kai to wpm
time_label = tk.Label(window, text="Start typing!")
time_label.pack(anchor=tk.E, padx=10)

# Se afto to Entry widget o xrhsths plhktrologei to keimeno
# Edw, dinoume kai onoma sto widget, gia na mporoume na xarakthrisoume ta events poy kanoume bind se afto
type_entry = tk.Entry(window, name="type_entry")

# Give focus to type_entry
type_entry.focus_set()
# Prepei na allaxoume th seira me thn opoia epexergazetai ta events h tkinter
# Etsi, to keimeno tha kataxwretai prin kalesoume th synarthsh poy elegxei to keimeno
type_entry.bindtags(("Entry", ".type_entry", ".", "all"))

# Kanoume bind sto <Key> event th synarthsh poy grapsame gia ton elegxo tou keimenou
# Kathe fora pou kapoio koumpi patietai mesa sto Entry, h on_entry_key tha kalestei
# me mia paramentro event, h opoia tha periexei ta dedomena tou gegonotos poy prokalese th klhsh ths synarthshs,
# opws pio plhktro paththike, se poio widget, an htan pathmeno to ctrl, Alt, Caps Lock, thesh pontikiou ktl
type_entry.bind("<Key>", on_entry_key)
type_entry.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# ekinhsh programmatos (event loop)  apo thn tkinter
window.mainloop()
