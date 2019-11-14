from tkinter import *
from tkinter import ttk

root = Tk()
scheduledimage=PhotoImage("...")
note = ttk.Notebook(root)

tab1 = ttk.Frame(note)
tab2 = ttk.Frame(note)
tab3 = ttk.Frame(note)

Button(tab1, text='Exit', command=root.destroy).pack(padx=100, pady=100)
#Button(tab2, text='help', command=root.destroy).pack(padx=100, pady=100)

note.add(tab1, text = "Tab One",image=scheduledimage, compound=TOP)
#note.add(tab1, text = "Tab One", compound=TOP)
note.add(tab2, text = "Tab Two")
note.add(tab3, text = "Tab Three")


note.pack()

root.mainloop()