from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class GuiMixin:
    def infobox(self, title, text, *args):              # use standard dialogs
        return showinfo(title, text)                    # *args for bkwd compat

    def errorbox(self, text):
        showerror('Error!', text)

    def question(self, title, text, *args):
        return askyesno(title, text)                    # return True or False

    def notdone(self):
        showerror('Not implemented', 'Option not available')

    def quit(self):
        ans = self.question('Verify quit', 'Are you sure you want to quit?')
        if ans:
            Frame.quit(self)                            # quit not recursive!

    def help(self):
        self.infobox('RTFM', 'See figure 1...')         # override this better

    def selectOpenFile(self, file="", dir="."):         # use standard dialogs
        return askopenfilename(initialdir=dir, initialfile=file)

    def selectSaveFile(self, file="", dir="."):
        return asksaveasfilename(initialfile=file, initialdir=dir)

    def clone(self, args=()):              # optional constructor args
        new = Toplevel()                   # make new in-process version of me
        myclass = self.__class__           # instance's (lowest) class object
        myclass(new, *args)                # attach/run instance to new window

    def browser(self, filename):                         
        new  = Toplevel()                                
        text = ScrolledText(new, height=30, width=85)    
        text.config(font=('courier', 10, 'normal'))      
        text.pack(expand=YES, fill=BOTH)
        new.title("Text Viewer")                         
        new.iconname("browser")
        text.insert('0.0', open(filename, 'r').read() )  

if __name__ == '__main__':

    class TestMixin(GuiMixin, Frame):      # standalone test
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack()
            Button(self, text='quit',  command=self.quit).pack(fill=X)
            Button(self, text='help',  command=self.help).pack(fill=X)
            #Button(self, text='clone', command=self.clone).pack(fill=X)
            #Button(self, text='spawn', command=self.other).pack(fill=X)

    TestMixin().mainloop()
