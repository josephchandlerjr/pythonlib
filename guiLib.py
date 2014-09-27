"""
Exports several custom tkinter widgets.

    GuiMenuMaker
    Quitter
    ScrolledCanvas
"""
from tkinter import *
from tkinter import messagebox


class GuiMenuMaker(Menu):                      
    """
        Wraps Menu widget. Adds commands and cascades based on 
        params argument. params data structure is as follows:
            params  => [menu, menu, ... ]
            menu    => (label, item)
            item    => callable | params
    """
    def __init__(self, params, parent=None):
        Menu.__init__(self, parent)
        parent.config(menu=self)
        for lbl, items in params:
            self.add_submenu(self, lbl, items)   # make submenu for each tuple in list

    def add_submenu(self, parent, lbl, items):
        """
            arguments:
                parent => parent widget of menu to be created
                lbl    => label of menu to be created
                items  => items to be added to menu
        """
        submenu = Menu(parent)
        self.add_items(submenu, items)
        parent.add_cascade(label=lbl, menu=submenu)

    def add_items(self, menu, items):
        """
            arguments:
                menu   => Menu instance
                items  => items to be added to menu
        """
        for (lbl, item) in items:
            if isinstance(item, list):
                self.add_submenu(menu, lbl, item)
            else:
                menu.add_command(label=lbl, command=item)

class Quitter(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)
        self.message = messagebox.askokcancel

    def quit(self):
        ans = self.message('Verify exit', "Really quit?")
        if ans: Frame.quit(self)

class ScrolledCanvas(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        
        self.canvas = Canvas(self, borderwidth=0, bg='tan')
        self.canvas.config(width=500, height=300)

        self.vsb = Scrollbar(self, command=self.canvas.yview)
        self.hsb = Scrollbar(self, orient='horizontal',command=self.canvas.xview)
        self.vsb.pack(side=RIGHT, fill=Y)
        self.hsb.pack(side=BOTTOM, fill=X)

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.canvas.pack(side=BOTTOM, expand=YES, fill=BOTH)

    def populate(self): # override me
        pass              

class ScrolledList(Frame):
    def __init__(self, options, bindings={}, parent=None):
        Frame.__init__(self, parent)
        self.start(bindings, packoptions=None)
        self.makeWidgets(options)

    def start(self, bindings={}, packoptions=None):
        self.bindings = bindings
        if not packoptions:
            self.pack(side=LEFT, expand=YES, fill=BOTH)
        else:
            self.pack(packoptions)

    def makeWidgets(self, options):
        sbar = Scrollbar(self)
        lst = Listbox(self, relief=SUNKEN)
        self.listbox = lst
        sbar.config(command=lst.yview)
        lst.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=BOTH)
        lst.pack(side=LEFT, expand=YES, fill=BOTH)
        pos = 0
        for label in options:
            lst.insert(pos, label)
            pos += 1
        lst.selection_set(0)
        for event_name, func in self.bindings.items():
            lst.bind(event_name, func)

class ScrolledMemberList(Frame):
    """
     initialized with a instance of Family and a function ondoubleclick 
     to bind to each item in the ScrolledList instance
    """
    def __init__(self, family, bindings={}, parent=None):
        Frame.__init__(self, parent)
        Label(self, text='%s family members' % family.lastname, relief=RAISED).pack(fill=X)
        self.scrolled_list = ScrolledList(family.members.keys(), bindings, self)
        self.listbox = self.scrolled_list.listbox
        self.pack(expand=YES, fill=BOTH)

class EntryForm(Toplevel):
    def __init__(self, fields, person=None):
        Toplevel.__init__(self)
        self.variables = {} 
        self.submit_state = False
        r = 0
        for field in fields:
            label = Label(self, width=20, text=field, relief=RIDGE)
            entry = Entry(self, relief=SUNKEN)
            label.grid(row=r, column=0)
            entry.grid(row=r, column=1)
            var = StringVar()
            entry.config(textvariable=var)
            self.variables[field] = var
            r += 1
        if person:                                               #if person already exists, populate
            for key in fields:
                try:
                    self.variables[key].set(getattr(person, key))
                except AttributeError:
                    pass
        Button(self, text='Submit', command=self.submit, relief=RAISED).grid(row=r, column=0)
        Button(self, text='Forget', command=self.destroy, relief=RAISED).grid(row=r, column=1)
        self.wait_visibility()
        self.focus_set()
        self.grab_set()
        self.wait_window()

    def submit(self):
        self.submit_state = True
        self.destroy()


