from tkinter import Tk, ttk, Frame, Button, Label, Entry, Text, Checkbutton, \
    Scale, Listbox, Menu, BOTH, RIGHT, RAISED, N, E, S, W, \
    HORIZONTAL, END, FALSE, IntVar, StringVar, messagebox as box

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("Simple Window")
        self.style = ttk.Style()
        print(self.style.theme_names())
        self.style.theme_use("xpnative")
        self.centreWindow()
        self.pack(fill=BOTH, expand=1)
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        firstNameLabel = Label(self, text="First Name")
        firstNameLabel.grid(row=0, column=0, sticky=W+E)
        lastNameLabel = Label(self, text="Last Name")
        lastNameLabel.grid(row=1, column=0, sticky=W+E)
        countryLabel = Label(self, text="Country")
        countryLabel.grid(row=2, column=0, sticky=W+E)
        addressLabel = Label(self, text="Address")
        addressLabel.grid(row=3, column=0, pady=10, sticky=W+E+N)
        
        firstNameText = Entry(self, width=20)
        firstNameText.grid(row=0, column=1, padx=5, pady=5, ipady=2, sticky=W+E)
        lastNameText = Entry(self, width=20)
        lastNameText.grid(row=1, column=1, padx=5, pady=5, ipady=2, sticky=W+E)
        
        self.countryVar = StringVar()
        self.countryCombo = ttk.Combobox(self, textvariable=self.countryVar)
        self.countryCombo['values'] = ('United States', 'United Kingdom', 'France')
        self.countryCombo.current(1)
        self.countryCombo.bind("<<ComboboxSelected>>", self.newCountry)
        self.countryCombo.grid(row=2, column=1, padx=5, pady=5, ipady=2, sticky=W)
        
        addressText = Text(self, padx=5, pady=5, width=20, height=6)
        addressText.grid(row=3, column=1, padx=5, pady=5, sticky=W)
        
        self.salaryVar = StringVar()
        salaryLabel = Label(self, text="Salary:", 
                            textvariable=self.salaryVar)
        salaryLabel.grid(row=0, column=2, columnspan=2, sticky=W+E)
        salaryScale = Scale(self, from_=10000, to=100000, orient=HORIZONTAL,
                            resolution=500, command=self.onSalaryScale)
        salaryScale.grid(row=1, column=2, columnspan=2, sticky=W+E)
        
        self.fullTimeVar = IntVar()
        fullTimeCheck = Checkbutton(self, text="Full-time?", 
                               variable=self.fullTimeVar, command=self.fullChecked)
        fullTimeCheck.grid(row=2, column=2, columnspan=2, sticky=W+E)
        #fullTimeCheck.select()
        
        self.titleVar = StringVar()
        self.titleVar.set("TBA")
        Label(self, textvariable=self.titleVar).grid(
            row=4, column=1, sticky=W+E
        )   # a reference to the label is not retained
        
        title = ['Programmer', 'Developer', 'Web Developer', 'Designer']
        titleList = Listbox(self, height=5)
        for t in title:
            titleList.insert(END, t)
        titleList.grid(row=3, column=2, columnspan=2, pady=5, sticky=N+E+S+W)
        titleList.bind("<<ListboxSelect>>", self.newTitle)
        
        okBtn = Button(self, text="OK", width=10, command=self.onConfirm)
        okBtn.grid(row=4, column=2, padx=5, pady=3, sticky=W+E)
        closeBtn = Button(self, text="Close", width=10, command=self.onExit)
        closeBtn.grid(row=4, column=3, padx=5, pady=3, sticky=W+E)
    
    def centreWindow(self):
        w = 500
        h = 300
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def onExit(self):
        self.quit()
    
    def newCountry(self, event):
        print(self.countryVar.get())
    
    def onSalaryScale(self, val):
        self.salaryVar.set("Salary: " + str(val))
    
    def fullChecked(self):
        if self.fullTimeVar.get() == 1:
            self.parent.title("Simple Window (full-time)")
        else:
            self.parent.title("Simple Window")
    
    def newTitle(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.titleVar.set(value)
    
    def onConfirm(self):
        box.showinfo("Information", "Thank you!")

def main():
    root = Tk()
    #root.geometry("250x150+300+300")    # width x height + x + y
    # we will use centreWindow instead
    root.resizable(width=FALSE, height=FALSE)
    # .. not resizable
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()

    # import tkinter
    # root = tkinter.Tk()
    # w=Button(root, text='ECE490 Capstone')
    # w.pack()
    # root.mainloop()
