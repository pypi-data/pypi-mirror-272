# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

import datetime

# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ...farm import Farm

class DistributionFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.left_frame = LeftFrame(master=self, 
                                    farm=self.farm)
        self.left_frame.grid(row=0, column=0, sticky='ewn')
        
        self.right_frame = None
        
    def refresh_right_frame(self, distribution_id=None):
        if self.right_frame is not None:
            self.right_frame.destroy()
            
        if distribution_id is not None:
            self.right_frame = RightFrame(master=self,
                                          farm=self.farm, 
                                          distribution_id=distribution_id)
            self.right_frame.grid(row=0, column=1, sticky='wn')
        
class LeftFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, **args):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master, **args)
        
        self.distribution_list_frame = DistributionListFrame(master=self, 
                                                     farm=self.farm)
        self.distribution_list_frame.grid(row=0, column=0, pady=5)
        
        self.create_distribution_label_frame = CreateDistributionLabelFrame(
            master=self.master, 
            farm=self.farm,
            distribution_list_frame=self.distribution_list_frame)
        self.create_distribution_label_frame.grid(row=1, column=0, pady=5)
    
        
class DistributionListFrame(ttk.Frame):
    
    def __init__(self, master, farm:Farm):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master)
        # GOODS LIST
        # define columns
        columns = ('date',)
        
        self.tree = ttk.Treeview(self, 
                                 columns=columns, 
                                 show='headings', 
                                 selectmode="browse",
                                 height=10)
        
        # define headings
        self.tree.heading('date', text='date', anchor=tk.W)

        # self.tree.column('date')
        
        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
    
    def fill(self):
        distribution = self.farm.sales.distribution.get_entries(columns=['id','date'], 
                                                     order_by='date DESC')
        
        for g in distribution:
            date = datetime.datetime.fromtimestamp(g[1])
            date_str = date.strftime('%d/%m/%Y')
            self.tree.insert('', tk.END, g[0], values=[date_str])
    
    def refresh(self, item_id=None, focus=True):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            if focus:
                self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def on_select(self, event):
        distribution_id = self.tree.focus()
        if len(distribution_id) > 0:
            print("you clicked on distribution id", distribution_id)
            
            self.master.master.refresh_right_frame(distribution_id=distribution_id)
            

class CreateDistributionLabelFrame(ttk.LabelFrame):
    def __init__(self, master, farm, distribution_list_frame=None):
        self.master = master
        self.farm = farm
        self.distribution_list_frame = distribution_list_frame
        
        ttk.LabelFrame.__init__(self, master, text="Nouveau")
                
        label_nom = ttk.Label(self, text="date JJ/MM/AAAA")
        label_nom.grid(sticky="W",row=0,column=0, padx=5, pady=5)
        
        self.new_date_value = tk.StringVar()
        ttk.Entry(self,
                  textvariable=self.new_date_value,
                  width=10)\
            .grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        button1 = ttk.Button(self, text = "Créer", command=self.new)
        button1.grid(sticky="W",row=1,column=1, padx=5, pady=5)
    
    def new(self):
        str_date = self.new_date_value.get()
        int_date = datetime.datetime.strptime(str_date, '%d/%m/%Y').timestamp()
        
        iid = self.farm.sales.distribution.insert_entry(date = int_date)
        
        if self.distribution_list_frame is not None:
            self.distribution_list_frame.refresh(item_id=iid)
        
        self.new_date_value.set(0)

class RightFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, distribution_id, **args):
        ttk.Frame.__init__(self, master, **args)
        
        self.farm = farm
        self.distribution_id = distribution_id
        
        data = self.farm.sales.distribution.get_entry(i=self.distribution_id)
        
        self.var = {}
        self.var['date'] = tk.StringVar()
        
        date = datetime.datetime.fromtimestamp(data['date'])
        date_str = date.strftime('%d/%m/%Y')
        self.var['date'].set(date_str)
        
        ttk.Label(self, text="Date", width=30)\
            .grid(row=0, column=0, padx=5, pady=2, sticky="w")
        entry=ttk.Entry(self, textvariable=self.var['date'])
        entry.grid(row=0, column=1, pady=2)
        entry.bind('<Return>', 
                self.save)
        entry.bind('<FocusOut>', 
                self.save)
        
        ttk.Label(self, text="Commentaire")\
            .grid(row=1, column=0, padx=5, pady=2, columnspan=2, sticky="w")
        self.note_widget = tk.Text(self, height=10, width=30)
        self.note_widget.grid(row=2, column=0, columnspan=2, sticky='ew', pady=2)
        
        self.note_widget.insert("end-1c",  data['note'])
        self.note_widget.bind('<FocusOut>', 
                self.save)
        
        
        # ttk.Button(self, text="Enregistrer", command=self.save)\
            # .grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=10)
            
        ttk.Button(self, text="Supprimer cette boulange", command=self.delete)\
            .grid(row=4, column=0, columnspan=2, sticky='e', padx=5, pady=30)
        
        
    def save(self, *args):
        str_date = self.var['date'].get()
        int_date = datetime.datetime.strptime(str_date, '%d/%m/%Y').timestamp()
        
        self.farm.sales.distribution.update_entry(
                            i= self.distribution_id,
                            date = int_date,
                            note = self.note_widget.get("1.0",'end-1c'))
        
        self.master.left_frame.distribution_list_frame.refresh(item_id=self.distribution_id,
                                                               focus=False)
    
    def delete(self, *args):
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ self.var['date'].get() +"\" ?"):
            self.farm.sales.distribution.delete_entry(i=self.distribution_id)
            
            self.master.left_frame.distribution_list_frame.refresh()
            self.master.refresh_right_frame()