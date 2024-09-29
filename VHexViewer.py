#! /usr/bin/python
# This is the Hex viewer
# Author    :   VenkataDurgaPrasad.B
# Email     :   durgababu21@gmail.com
#

import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from VUtil import VHexDump

class vHexViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        ico_file = "VHexViewer.png"
        if os.path.isfile(ico_file):
            ico = tk.PhotoImage(file=ico_file)
            self.iconphoto(True, ico)
        self.title("Hex Viewer")
        #create a menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        self.option_add('*tearOff', False)
        # bind keys with event handler
        self.bind_all("<Control-o>", self.KeyBinding)
        self.bind_all("<Control-q>", self.KeyBinding)
        self.bind_all("<Control-d>", self.KeyBinding)
        #add sub menu File to menubar
        m_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=m_file)
        #add options under file
        m_file.add_command(label="OpenFile", command=self.OpenFile)
        m_file.entryconfigure('OpenFile', accelerator='Ctrl+o')
        m_file.add_command(label="CloseFile", command=self.CloseFile)
        m_file.entryconfigure('CloseFile', accelerator='Ctrl+d')
        m_file.add_separator()
        m_file.add_command(label="Exit", command=self.OnExit)
        m_file.entryconfigure('Exit', accelerator='Ctrl+q')
        #add sub menu help to menubar
        m_help = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="Help", menu=m_help)
        #add options under Help
        m_help.add_command(label="About", command=self.About)
        # create frame
        self.w_tabframe_hdr = tk.Frame(self)
        self.w_tabframe_hdr.pack(fill="both")
        self.w_tabframe_data = tk.Frame(self)
        self.w_tabframe_data.pack(expand=True, fill="both")
        self.CurFile = None
        self.w_buttons = []
        self.w_hexview = []
    
    def OpenFile(self):
        InFile = filedialog.askopenfilename(title="Select binary File", filetypes=[("bin files", "*.bin"), ("All files", "*.*")])
        if InFile:
            print ("Selected bin file:", InFile)
            self.CreateTab(InFile)

    def CreateTab(self, InFile):
        w_NewTab = tk.Frame(self.w_tabframe_data)
        w_NewTab.pack(fill="both", expand=True, padx=5, pady=5)
        # create status bar
        w_status_bar = tk.Label(w_NewTab, text="", padx=5, pady=5, anchor="se")
        w_status_bar.pack(side="bottom")
        #create a new text widget to show hex data
        w_text = tk.Text(w_NewTab, padx=5, pady=5)
        w_text.pack(expand=True, fill="both")
        w_scrollbar = tk.Scrollbar(w_text, relief="solid", command=w_text.yview, cursor="arrow")
        w_scrollbar.pack(side="right", fill="y")
        w_text.configure(yscrollcommand=w_scrollbar.set)
        if not InFile:
            w_text.config(state="disabled")
            return
        tab_name = InFile.split("/")[-1]
        # Create a button to select the tab
        w_tabButton = tk.Button(self.w_tabframe_hdr, text=tab_name, command=lambda: self.SelectTab(w_NewTab))
        w_tabButton.pack(side="left", padx=5, pady=5)
        w_tabButton.configure(bg="grey")
        # display file contents
        with open(InFile, 'rb') as InfileHandle:
            TotalSize = os.stat(InFile).st_size
            w_text.config(state="normal")
            w_text.delete("1.0", tk.END)
            VHData = VHexDump(InfileHandle, TotalSize)
            for i in VHData:
                w_text.insert(tk.END, i)
                w_text.insert(tk.END, "\n")
            w_text.config(state="disabled")
            InfileHandle.close()
        w_status_bar.config(text=f"size: ({hex(TotalSize)}){TotalSize} Bytes", justify="right")
        # add the new tab to the tablist
        self.w_hexview.append(w_NewTab)
        self.w_buttons.append(w_tabButton)
        self.SelectTab(w_NewTab)
        return
    
    def SelectTab(self, tab):
        for w in self.w_hexview:
            w.pack_forget()
        if self.CurFile:
            idx = self.w_hexview.index(self.CurFile)
            self.w_buttons[idx].configure(bg="grey", fg="white")
        self.CurFile = tab
        tab.pack(fill="both", expand=True, padx=5, pady=5)
        idx = self.w_hexview.index(tab)
        self.w_buttons[idx].configure(bg="green", fg="white")

        return
    
    def CloseFile(self):
        # Close the currently selected file
        if self.CurFile:
            idx = self.w_hexview.index(self.CurFile)
            self.w_hexview.remove(self.CurFile)
            self.CurFile.destroy()
            self.CurFile = None
            tmp = self.w_buttons[idx]
            self.w_buttons.remove(tmp)
            tmp.destroy()
            # Select the next tab or the previous tab if the last tab was closed
            if idx < len(self.w_hexview):
                self.SelectTab(self.w_hexview[idx])
            elif len(self.w_hexview) > 0:
                self.SelectTab(self.w_hexview[-1])
        return
    
    def KeyBinding(self, event):
        if (event.keysym == 'o'):
            self.OpenFile()
        if (event.keysym == 'q'):
            self.OnExit()
        if (event.keysym == 'd'):
            self.CloseFile()
        return
    
    def OnExit(self):
        self.destroy()
        return
    
    def About(self):
        messagebox.showinfo(message="Hex Viewer V1.0",
                            detail="This tool is used to view the binary file in hex fomat",
                            title="HexViewer help")
        return

# This is the main entry
if __name__ == '__main__':
    HViewer = vHexViewer()
    HViewer.mainloop()
