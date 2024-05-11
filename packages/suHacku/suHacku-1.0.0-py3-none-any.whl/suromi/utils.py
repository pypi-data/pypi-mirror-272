from .curses import courser

def total_duration():

    return sum(i.duration for i in courser)
