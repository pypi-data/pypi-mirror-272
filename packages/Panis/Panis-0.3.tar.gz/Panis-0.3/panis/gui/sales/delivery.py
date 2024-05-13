# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

# import os
# # import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ...farm import Farm

class DeliveryFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.left_frame = LeftFrame(master=self, 
                                    farm=self.farm)
        self.left_frame.grid(row=0, column=0, sticky='ew')
        
        self.right_frame = None
        
    def refresh_right_frame(self, delivery_id=None):
        if self.right_frame is not None:
            self.right_frame.destroy()
            
        if delivery_id is not None:
            self.right_frame = RightFrame(master=self,
                                          farm=self.farm, 
                                          delivery_id=delivery_id)
            self.right_frame.grid(row=0, column=1, sticky='wn')
        
class LeftFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, **args):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master, **args)
        
        self.delivery_list_frame = DeliveryListFrame(master=self, 
                                                     farm=self.farm)
        self.delivery_list_frame.grid(row=1, column=0, pady=5)
        
        self.create_delivery_frame = CreateDeliveryFrame(
            master=self, 
            farm=self.farm,
            delivery_list_frame=self.delivery_list_frame)
        self.create_delivery_frame.grid(row=0, column=0, pady=5, sticky='w')
        
class DeliveryListFrame(ttk.Frame):
    
    def __init__(self, master, farm:Farm):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master)
        # GOODS LIST
        # define columns
        columns = ('name')
        
        self.tree = ttk.Treeview(self, 
                                 columns=columns, 
                                 show='headings', 
                                 selectmode="browse",
                                 height=20)
        
        # define headings
        self.tree.heading('name', text='nom', anchor=tk.W)
        
        # self.tree.column('name')
        
        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
    
    def fill(self):
        delivery = self.farm.sales.delivery.get_entries(columns=['id','name'], 
                                                     order_by="position DESC, UPPER(name)")
        
        for g in delivery:
            self.tree.insert('', tk.END, g[0], values=g[1:])
    
    def refresh(self, item_id=None, focus=True):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            if focus:
                self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def on_select(self, event):
        delivery_id = self.tree.focus()
        if len(delivery_id) > 0:
            print("you clicked on delivery id", delivery_id)
            
            self.master.master.refresh_right_frame(delivery_id=delivery_id)

class CreateDeliveryFrame(ttk.Frame):
    def __init__(self, master, farm, delivery_list_frame=None):
        self.master = master
        self.farm = farm
        self.delivery_list_frame = delivery_list_frame
        
        ttk.Frame.__init__(self, master)
                
        # label_nom = ttk.Label(self, text="nom")
        # label_nom.grid(sticky="W",row=0,column=0, padx=5, pady=5)
        
        # self.new_name_value = tk.StringVar()
        
        # entry_nom = ttk.Entry(self, width=20, 
                             # textvariable=self.new_name_value)
        # entry_nom.grid(sticky="W",row=1,column=0, padx=5, pady=5)
        
        button1 = ttk.Button(self, text = "+", command=self.new, width=2)
        button1.grid(sticky="ew", row=0, column=0, padx=5, pady=5)
    
    def new(self):
        iid = self.farm.sales.delivery.insert_entry(name = 'Nouvelle Livraison')
        
        if self.delivery_list_frame is not None:
            self.delivery_list_frame.refresh(item_id=iid)
        
        self.new_name_value.set('')

class RightFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, delivery_id, **args):
        ttk.Frame.__init__(self, master, **args)
        
        self.farm = farm
        self.delivery_id = delivery_id
        
        data = self.farm.sales.delivery.get_entry(i=self.delivery_id)
        
        self.var = {}
        self.var['name'] = tk.StringVar()
        self.var['position'] = tk.DoubleVar()
        self.var['address'] = tk.StringVar()
        self.var['postal_code'] = tk.IntVar()
        self.var['city'] = tk.StringVar()
        self.var['new_page'] = tk.BooleanVar()
        self.var['unsold_line'] = tk.BooleanVar()
        self.var['market_sheet'] = tk.BooleanVar()
        
        for key, var in self.var.items():
            var.set(data[key])
        
        ttk.Label(self, text="Nom", width=30)\
            .grid(row=0, column=0, padx=5, pady=2, sticky="w")
        entry = ttk.Entry(self, textvariable=self.var['name'])
        entry.grid(row=0, column=1, pady=2)
        entry.bind('<Return>', 
                self.save)
        entry.bind('<FocusOut>', 
                self.save)
            
        ttk.Label(self, text="#", width=5)\
            .grid(row=1, column=0, padx=5, pady=2, sticky="w")
        entry=ttk.Entry(self, textvariable=self.var['position'])
        entry.grid(row=1, column=1, pady=2)
        entry.bind('<Return>', 
                self.save)
        entry.bind('<FocusOut>', 
                self.save)
            
        ttk.Label(self, text="Adresse", width=30)\
            .grid(row=2, column=0, padx=5, pady=2, sticky="w")
        entry=ttk.Entry(self, textvariable=self.var['address'])
        entry.grid(row=2, column=1, pady=2)
        entry.bind('<Return>', 
                self.save)
        entry.bind('<FocusOut>', 
                self.save)
        
        ttk.Label(self, text="Code postal", width=5)\
            .grid(row=3, column=0, padx=5, pady=2, sticky="w")
        entry=ttk.Entry(self, textvariable=self.var['postal_code'])
        entry.grid(row=3, column=1, pady=2)
        entry.bind('<Return>', 
                self.save)
        entry.bind('<FocusOut>', 
                self.save)
        
        ttk.Label(self, text="Ville", width=30)\
            .grid(row=4, column=0, padx=5, pady=2, sticky="w")
        entry=ttk.Entry(self, textvariable=self.var['city'])
        entry.grid(row=4, column=1, pady=2)
        entry.bind('<Return>', 
                self.save)
        entry.bind('<FocusOut>', 
                self.save)
        
        ttk.Checkbutton(self, 
                        text='Nouvelle page de rapport', 
                        variable=self.var['new_page'], 
                        command=self.save)\
            .grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        
        ttk.Checkbutton(self, 
                        text='Ligne retours', 
                        variable=self.var['unsold_line'], 
                        command=self.save)\
            .grid(row=6, column=0, columnspan=2, padx=5, pady=2, sticky="w")
            
        ttk.Checkbutton(self, 
                        text='feuille de marché', 
                        variable=self.var['market_sheet'], 
                        command=self.save)\
            .grid(row=7, column=0, columnspan=2, padx=5, pady=2, sticky="w")
            
        
        ttk.Label(self, text="Commentaire")\
            .grid(row=8, column=0, padx=5, pady=2, columnspan=2, sticky="w")
        self.note_widget = tk.Text(self, height=10, width=30)
        self.note_widget.grid(row=9, column=0, columnspan=2, sticky='ew', pady=2)
        
        self.note_widget.insert("end-1c",  data['note'])
        self.note_widget.bind('<FocusOut>', 
                              self.save)
        
        # ttk.Button(self, text="Enregistrer", command=self.save)\
            # .grid(row=7, column=0, columnspan=2, sticky='w', padx=5, pady=10)
            
        ttk.Button(self, text="Supprimer cette livraison", command=self.delete)\
            .grid(row=10, column=0, columnspan=2, sticky='e', padx=5, pady=30)
        
        
    def save(self, *args):
        self.farm.sales.delivery.update_entry(
                            i= self.delivery_id,
                            name = self.var['name'].get(),
                            position = self.var['position'].get(),
                            address = self.var['address'].get(),
                            postal_code = self.var['postal_code'].get(),
                            city = self.var['city'].get(),
                            new_page = int(self.var['new_page'].get()),
                            unsold_line = int(self.var['unsold_line'].get()),
                            market_sheet = int(self.var['market_sheet'].get()),
                            note = self.note_widget.get("1.0",'end-1c'))
        
        self.master.left_frame.delivery_list_frame.refresh(item_id=self.delivery_id,
                                                           focus=False)
    
    def delete(self, *args):
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ self.var['name'].get() +"\" ?"):
            self.farm.sales.delivery.delete_entry(i=self.delivery_id)
            
            self.master.left_frame.delivery_list_frame.refresh()
            self.master.refresh_right_frame()