# -*- coding: utf-8 -*-

import tkinter as Tk

def table_scroll_Y(self, *args):
        self.table_title.yview
        self.table_data.yview
def build_table(self, cols, data):
    for child in self.tablebase.winfo_children(): # Clear existing table
        child.pack_forget()
        child.destroy()
    colour1 = "#EEEEEE" # sets title colour
    rheight = 1 # sets row height
    rowsize = []

    #Note: self.tku.cFrame(**kwrds) =  Frame(*args) and frame.pack(*args)
    layout1=self.tku.cFrame(self.tablebase, side=LEFT,  fill=BOTH, expand=1, bg="white") #split between table area and scroll bar for fixed Y scroll
    self.Vscroll = Scrollbar(self.tablebase, orient="vertical")
    self.Vscroll.pack(side=RIGHT, fill=Y)
    layout2 = self.tku.cFrame(layout1, side=TOP, fill=BOTH, expand=1, bg="white") #split between table and bottom scroll for fixed X scroll
    self.Hscroll = Scrollbar(layout1, orient="horizontal")
    self.Hscroll.pack(side=BOTTOM, fill=X)

    self.table_title = Canvas(layout2, bg="red", highlightthickness=0, height=10) #X scroll area for Column titles
    self.table_data = Canvas(layout2, bg="blue", highlightthickness=0, yscrollcommand=self.Vscroll.set, xscrollcommand=self.Hscroll.set) # XY scroll area for table data
    self.Vscroll.config(command = self.table_scroll_Y) #configures command for Y on both scroll areas
    self.Hscroll.config(command = self.table_data.xview) #configure command for X on data scroll region

    #crate frames to hold all the widgets
    title_frame = Frame(self.table_title, bg="orange")
    title_frame.pack(padx=15, pady=15, fill=BOTH, expand=1)
    data_frame = Frame(self.table_data, bg="purple")
    data_frame.pack(padx=15, pady=15, fill=BOTH, expand=1)
    
    #create windows and pack widgets
    self.table_title.pack(side=TOP, fill=X, padx=5, pady=5)
    self.table_data.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)
    self.table_title.create_window(0,0, window=title_frame)
    self.table_data.create_window(0,0, window=data_frame)
    self.table_title.config(scrollregion=self.table_title.bbox("all"))
    self.table_data.config(scrollregion=self.table_data.bbox("all"))
    self.table_title.yview_moveto(0) 
    self.table_data.yview_moveto(0)
    self.table_data.xview_moveto(0)

    #Build table column headers
    row = self.tku.cFrame(title_frame, fill=X, borderwidth=1, relief="ridge", highlightbackground="black")
    for item in cols:
        Label(row, text=item, width=len(item)+1, borderwidth=2, relief="groove", heigh=rheight, bg=colour1).pack(side=LEFT, fill=X, expand=1)
        rowsize.append(len(item)+1)

    #Build table data
    i = 0
    for datarow in data:
        row = self.tku.cFrame(data_frame, fill=X, borderwidth=1, relief="ridge", highlightbackground="black")
        for key, value in datarow.items():
            Label(row, text=value, width=rowsize[i], borderwidth=2, relief="groove", heigh=rheight, bg="white").pack(side=LEFT, fill=X, expand=1)
            if i <= len(rowsize):
                i = 0
            else:
                i+=1