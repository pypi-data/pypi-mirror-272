# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ...farm import Farm

class ShapeFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.left_frame = LeftFrame(master=self, 
                                    farm=self.farm)
        self.left_frame.grid(row=0, column=0, sticky='ewn')
        
        self.right_frame = None
        
    def refresh_right_frame(self, shape_id=None):
        if self.right_frame is not None:
            self.right_frame.destroy()
            
        if shape_id is not None:
            self.right_frame = RightFrame(master=self,
                                          farm=self.farm, 
                                          shape_id=shape_id)
            self.right_frame.grid(row=0, column=1, sticky='wn')
        
class LeftFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, **args):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master, **args)
        
        self.shape_list_frame = ShapeListFrame(master=self, 
                                                     farm=self.farm)
        self.shape_list_frame.grid(row=0, column=0, pady=5)
        
        # self.create_shape_label_frame = CreateShapeLabelFrame(
        #     master=self.master, 
        #     farm=self.farm,
        #     shape_list_frame=self.shape_list_frame)
        # self.create_shape_label_frame.grid(row=1, column=0, pady=5)
        
        button1 = ttk.Button(self, text = "+", command=self.new)
        button1.grid(sticky="WE",row=1,column=0, padx=5, pady=5)
        
    def new(self):
        iid = self.farm.bakery.shape.insert_entry(name = "Nouveau",
                                                 code = "NEW")
        
        self.shape_list_frame.refresh(item_id=iid)
        
class ShapeListFrame(ttk.Frame):
    
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
                                 height=18)
        
        # define headings
        self.tree.heading('name', text='name', anchor=tk.W)
        self.tree.heading('position', text='#', anchor=tk.E)
        
        self.tree.column('name', width=150, anchor=tk.W)
        self.tree.column('position', width=20, anchor=tk.E)
        
        # self.tree.column('date')
        
        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
    
    def fill(self):
        shape = self.farm.bakery.shape.get_entries(columns=['id','name', 'position'], 
                                                     order_by='position DESC, name')
        
        for g in shape:
            self.tree.insert('', tk.END, g[0], values=g[1:])
    
    def refresh(self, item_id=None):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def on_select(self, event):
        shape_id = self.tree.focus()
        if len(shape_id) > 0:
            print("you clicked on shape id", shape_id)
            
            self.master.master.refresh_right_frame(shape_id=shape_id)
            

# class CreateShapeLabelFrame(ttk.LabelFrame):
#     def __init__(self, master, farm, shape_list_frame=None):
#         self.master = master
#         self.farm = farm
#         self.shape_list_frame = shape_list_frame
        
#         ttk.LabelFrame.__init__(self, master, text="Nouveau")
                
#         label_nom = ttk.Label(self, text="nom")
#         label_nom.grid(sticky="W",row=0,column=0, padx=5, pady=5)
        
#         self.new_name_value = tk.StringVar()
#         ttk.Entry(self,
#                   textvariable=self.new_name_value,
#                   width=10)\
#             .grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
#         button1 = ttk.Button(self, text = "Créer", command=self.new)
#         button1.grid(sticky="W",row=1,column=1, padx=5, pady=5)
    
#     def new(self):
#         iid = self.farm.bakery.shape.insert_entry(name = self.new_name_value.get(),
#                                                  code = self.new_name_value.get())
        
#         if self.shape_list_frame is not None:
#             self.shape_list_frame.refresh(item_id=iid)
        
#         self.new_name_value.set('')

class RightFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, shape_id, **args):
        ttk.Frame.__init__(self, master, **args)
        
        self.farm = farm
        self.shape_id = shape_id
        
        data = self.farm.bakery.shape.get_entry(i=self.shape_id)
        
        self.var = {}
        self.var['name'] = tk.StringVar(value=data['name'])
        self.var['code'] = tk.StringVar(value=data['code'])
        self.var['position'] = tk.DoubleVar(value=data['position'])
        
        ttk.Label(self, text="nom")\
            .grid(row=0, column=0, padx=5, pady=2, sticky="w")
        entry_name = ttk.Entry(self, textvariable=self.var['name'], width=30)
        entry_name.grid(row=0, column=1, pady=2, sticky="w")
        entry_name.bind('<Return>', 
                self.save_and_refresh)
        entry_name.bind('<FocusOut>', 
                self.save_and_refresh)
            
        ttk.Label(self, text="code")\
            .grid(row=1, column=0, padx=5, pady=2, sticky="w")
        entry_code = ttk.Entry(self, textvariable=self.var['code'], width=8)
        entry_code.grid(row=1, column=1, pady=2, sticky="w")
        entry_code.bind('<Return>', 
                self.save)
        entry_code.bind('<FocusOut>', 
                self.save)
            
        ttk.Label(self, text="#")\
            .grid(row=2, column=0, padx=5, pady=2, sticky="w")
        entry_position=ttk.Entry(self, textvariable=self.var['position'], width=5)
        entry_position.grid(row=2, column=1, pady=2, sticky="w")
        entry_position.bind('<Return>', 
                self.save_and_refresh)
        entry_position.bind('<FocusOut>', 
                self.save_and_refresh)
        
        ttk.Button(self, text="Supprimer ce format", command=self.delete)\
            .grid(row=3, column=0, columnspan=2, sticky='e', padx=5, pady=30)
        
        
    def save(self, *args):
        self.farm.bakery.shape.update_entry(
                            i= self.shape_id,
                            name = self.var['name'].get(),
                            code = self.var['code'].get(),
                            position = self.var['position'].get())
        
        
    def save_and_refresh(self, *args):
        self.save()
        self.master.left_frame.shape_list_frame.refresh(item_id=self.shape_id)
    
    def delete(self, *args):
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ self.var['name'].get() +"\" ?"):
            self.farm.bakery.shape.delete_entry(i=self.shape_id)
            
            self.master.left_frame.shape_list_frame.refresh()
            self.master.refresh_right_frame()