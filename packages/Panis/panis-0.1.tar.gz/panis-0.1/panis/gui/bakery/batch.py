# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ...farm import Farm

class BatchFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.left_frame = LeftFrame(master=self, 
                                    farm=self.farm)
        self.left_frame.grid(row=0, column=0, sticky='ew')
        
        self.right_frame = None
        
    def refresh_right_frame(self, batch_id=None):
        if self.right_frame is not None:
            self.right_frame.destroy()
            
        if batch_id is not None:
            self.right_frame = RightFrame(master=self,
                                          farm=self.farm, 
                                          batch_id=batch_id)
            self.right_frame.grid(row=0, column=1, sticky='wn')
        
class LeftFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, **args):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master, **args)
        
        self.batch_list_frame = BatchListFrame(master=self, 
                                                     farm=self.farm)
        self.batch_list_frame.grid(row=0, column=0, pady=5)
        
        button1 = ttk.Button(self, text = "+", command=self.new)
        button1.grid(sticky="WE",row=1,column=0, padx=5, pady=5)
    
    def new(self):
        iid = self.farm.bakery.batch.insert_entry(name = "Nouveau",
                                                 code = "NEW")
        
        self.batch_list_frame.refresh(item_id=iid)
        
        
class BatchListFrame(ttk.Frame):
    
    def __init__(self, master, farm:Farm):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master)
        # GOODS LIST
        # define columns
        columns = ('name', 'position')
        
        self.tree = ttk.Treeview(self, 
                                 columns=columns, 
                                 show='headings', 
                                 selectmode="browse",
                                 height=20)
        
        # define headings
        self.tree.heading('name', text='nom', anchor=tk.W)
        self.tree.heading('position', text='#', anchor=tk.E)
        
        self.tree.column('position', width=30, anchor=tk.E)
        
        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
    
    def fill(self):
        batch = self.farm.bakery.batch.get_entries(columns=['id','name', 'position'], 
                                                     order_by='position DESC, name')
        
        for g in batch:
            self.tree.insert('', tk.END, g[0], values=g[1:])
    
    def refresh(self, item_id=None):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def on_select(self, event):
        batch_id = self.tree.focus()
        if len(batch_id) > 0:
            print("you clicked on batch id", batch_id)
            
            self.master.master.refresh_right_frame(batch_id=batch_id)
            

class RightFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, batch_id, **args):
        ttk.Frame.__init__(self, master, **args)
        
        self.farm = farm
        self.batch_id = batch_id
        
        data = self.farm.bakery.batch.get_entry(i=self.batch_id)
        
        self.var = {}
        self.var['name'] = tk.StringVar()
        self.var['code'] = tk.StringVar()
        self.var['position'] = tk.DoubleVar()
        
        for key in self.var.keys():
            self.var[key].set(data[key])
        
        ttk.Label(self, text="Nom")\
            .grid(row=0, column=0, padx=5, pady=2, sticky="w")
        entry_name = ttk.Entry(self, textvariable=self.var['name'])
        entry_name.grid(row=0, column=1, pady=2)
        entry_name.bind('<Return>', 
                self.save_and_refresh)
        entry_name.bind('<FocusOut>', 
                self.save_and_refresh)
            
        ttk.Label(self, text="code")\
            .grid(row=1, column=0, padx=5, pady=2, sticky="w")
        entry_code=ttk.Entry(self, textvariable=self.var['code'], width=5)
        entry_code.grid(row=1, column=1, pady=2)
        entry_code.bind('<Return>', 
                self.save)
        entry_code.bind('<FocusOut>', 
                self.save)
            
        ttk.Label(self, text="#")\
            .grid(row=2, column=0, padx=5, pady=2, sticky="w")
        entry_position=ttk.Entry(self, textvariable=self.var['position'])
        entry_position.grid(row=2, column=1, pady=2)
        entry_position.bind('<Return>', 
                self.save_and_refresh)
        entry_position.bind('<FocusOut>', 
                self.save_and_refresh)
            
        ttk.Label(self, text="Commentaire")\
            .grid(row=4, column=0, padx=5, pady=2, columnspan=2, sticky="w")
        self.note_widget = tk.Text(self, height=10, width=30)
        self.note_widget.grid(row=5, column=0, columnspan=2, sticky='ew', pady=2)
        
        self.note_widget.insert("end-1c",  data['note'])
        self.note_widget.bind('<FocusOut>', 
                self.save)
        
        # ttk.Button(self, text="Enregistrer", command=self.save)\
            # .grid(row=6, column=0, columnspan=2, sticky='w', padx=5, pady=10)
            
        ttk.Button(self, text="Supprimer cette cuisson", command=self.delete)\
            .grid(row=7, column=0, columnspan=2, sticky='e', padx=5, pady=30)
        
        
    def save(self, *args):
        self.farm.bakery.batch.update_entry(
                            i= self.batch_id,
                            name = self.var['name'].get(),
                            code = self.var['code'].get(),
                            position = self.var['position'].get(),
                            note = self.note_widget.get("1.0",'end-1c'))
        
    def save_and_refresh(self, *args):
        self.save()
        self.master.left_frame.batch_list_frame.refresh(item_id=self.batch_id)
    
    def delete(self, *args):
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ self.var['name'].get() +"\" ?"):
            self.farm.bakery.batch.delete_entry(i=self.batch_id)
            
            self.master.left_frame.batch_list_frame.refresh()
            self.master.refresh_right_frame()