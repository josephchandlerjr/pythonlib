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

class MyListbox(Listbox):
    'Listbox with a get_selected method'
    def __init__(self, parent=None, **options):
        Listbox.__init__(self, parent, **options)

    def get_selected(self):
        index = self.curselection()
        return self.get(index)

    def get_selected_right_click(self, event):
        index = self.nearest(event.y)
        return self.get(index)

class ScrolledList(Frame):
    def __init__(self, options, bindings={}, parent=None):
        Frame.__init__(self, parent)
        self.bindings = bindings
        self.pack(side=LEFT, expand=YES, fill=BOTH)
        self.makeWidgets(options)

    def makeWidgets(self, options):
        sbar = Scrollbar(self)
        lst = MyListbox(self, relief=SUNKEN)
        self.listbox = lst
        sbar.config(command=lst.yview)
        lst.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=BOTH)
        lst.pack(side=LEFT, expand=YES, fill=BOTH)
        for pos, label in enumerate(options):
            lst.insert(pos, label)
        lst.selection_set(0)
        
