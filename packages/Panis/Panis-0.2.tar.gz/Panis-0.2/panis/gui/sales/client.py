# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno


# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ...farm import Farm

class ClientFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.left_frame = LeftFrame(master=self, 
                                    farm=self.farm)
        self.left_frame.grid(row=0, column=0, sticky='ew')
        
        self.right_frame = None
        
    def refresh_right_frame(self, client_id=None):
        if self.right_frame is not None:
            self.right_frame.destroy()
            
        if client_id is not None:
            self.right_frame = RightFrame(master=self,
                                          farm=self.farm, 
                                          client_id=client_id)
            self.right_frame.grid(row=0, column=1, sticky='wn')
        
class LeftFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, **args):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master, **args)
        
        self.client_list_frame = ClientListFrame(master=self, 
                                                     farm=self.farm)
        self.client_list_frame.grid(row=1, column=0, pady=5)
        
        self.create_client_label_frame = CreateClientLabelFrame(
            master=self, 
            farm=self.farm,
            client_list_frame=self.client_list_frame)
        self.create_client_label_frame.grid(row=0, column=0, pady=5, sticky='w')
    
        
class ClientListFrame(ttk.Frame):
    
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

        self.tree.column('name', width=200)
        
        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
    
    def fill(self):
        client = self.farm.sales.client.get_entries(columns=['id',"name || ' ' || first_name as full_name"], 
                                                     order_by='UPPER(full_name)')
        
        for g in client:
            self.tree.insert('', tk.END, g[0], values=g[1:])
    
    def refresh(self, item_id=None, focus=True):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            if focus:
                self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def on_select(self, event):
        client_id = self.tree.focus()
        if len(client_id) > 0:
            print("you clicked on client id", client_id)
            
            self.master.master.refresh_right_frame(client_id=client_id)
            

class CreateClientLabelFrame(ttk.Frame):
    def __init__(self, master, farm, client_list_frame=None):
        self.master = master
        self.farm = farm
        self.client_list_frame = client_list_frame
        
        ttk.Frame.__init__(self, master)
                
        button1 = ttk.Button(self, text = "+", command=self.new, width=2)
        button1.grid(sticky="W",row=0,column=0, padx=5, pady=5)
        
    def new(self):
        iid = self.farm.sales.client.insert_entry(name = 'Nouveau Client')
        
        if self.client_list_frame is not None:
            self.client_list_frame.refresh(item_id=iid)
        
        self.new_name_value.set('')

class RightFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, client_id, **args):
        ttk.Frame.__init__(self, master, **args)
        
        self.farm = farm
        self.client_id = client_id
        
        data = self.farm.sales.client.get_entry(i=self.client_id)
        
        self.var = {}
        self.var['name'] = tk.StringVar()
        self.var['first_name'] = tk.StringVar()
        self.var['phone'] = tk.StringVar()
        self.var['address'] = tk.StringVar()
        self.var['postal_code'] = tk.IntVar()
        self.var['city'] = tk.StringVar()
        
        for key in self.var.keys():
            self.var[key].set(data[key])
        
        ttk.Label(self, text="Nom", width=30)\
            .grid(row=0, column=0, padx=5, pady=2, sticky="w")
        entry_name = ttk.Entry(self, textvariable=self.var['name'])
        entry_name.grid(row=0, column=1, pady=2)
        entry_name.bind('<Return>', 
                self.save)
        entry_name.bind('<FocusOut>', 
                self.save)
            
        ttk.Label(self, text="Prénom", width=30)\
            .grid(row=1, column=0, padx=5, pady=2, sticky="w")
        entry_first_name = ttk.Entry(self, textvariable=self.var['first_name'])
        entry_first_name.grid(row=1, column=1, pady=2)
        entry_first_name.bind('<Return>', 
                self.save)
        entry_first_name.bind('<FocusOut>', 
                self.save)
            
        ttk.Label(self, text="Téléphone", width=30)\
            .grid(row=2, column=0, padx=5, pady=2, sticky="w")
        entry_phone = ttk.Entry(self, textvariable=self.var['phone'])
        entry_phone.grid(row=2, column=1, pady=2)
        entry_phone.bind('<Return>', 
                self.save)
        entry_phone.bind('<FocusOut>', 
                self.save)
            
        ttk.Label(self, text="Adresse", width=30)\
            .grid(row=3, column=0, padx=5, pady=2, sticky="w")
        entry_address = ttk.Entry(self, textvariable=self.var['address'])
        entry_address.grid(row=3, column=1, pady=2)
        entry_address.bind('<Return>', 
                self.save)
        entry_address.bind('<FocusOut>', 
                self.save)
        
        ttk.Label(self, text="Code postal", width=5)\
            .grid(row=4, column=0, padx=5, pady=2, sticky="w")
        entry_postal_code = ttk.Entry(self, textvariable=self.var['postal_code'])
        entry_postal_code.grid(row=4, column=1, pady=2)
        entry_postal_code.bind('<Return>', 
                self.save)
        entry_postal_code.bind('<FocusOut>', 
                self.save)
        
        ttk.Label(self, text="Ville", width=30)\
            .grid(row=5, column=0, padx=5, pady=2, sticky="w")
        entry_city = ttk.Entry(self, textvariable=self.var['city'])
        entry_city.grid(row=5, column=1, pady=2)
        entry_city.bind('<Return>', 
                self.save)
        entry_city.bind('<FocusOut>', 
                self.save)
        
        ttk.Label(self, text="Commentaire")\
            .grid(row=6, column=0, padx=5, pady=2, columnspan=2, sticky="w")
        self.note_widget = tk.Text(self, height=10, width=30)
        self.note_widget.grid(row=7, column=0, columnspan=2, sticky='ew', pady=2)
        
        self.note_widget.insert("end-1c",  data['note'])
        
        self.note_widget.bind('<FocusOut>', 
                self.save)
        
        # ttk.Button(self, text="Enregistrer", command=self.save)\
            # .grid(row=8, column=0, columnspan=2, sticky='w', padx=5, pady=10)
            
        ttk.Button(self, text="Supprimer ce client", command=self.delete)\
            .grid(row=9, column=0, columnspan=2, sticky='e', padx=5, pady=30)
        
        
    def save(self, *args):
        self.farm.sales.client.update_entry(
                            i= self.client_id,
                            name = self.var['name'].get(),
                            first_name = self.var['first_name'].get(),
                            phone = self.var['phone'].get(),
                            address = self.var['address'].get(),
                            postal_code = self.var['postal_code'].get(),
                            city = self.var['city'].get(),
                            note = self.note_widget.get("1.0",'end-1c'))
        
        self.master.left_frame.client_list_frame.refresh(item_id=self.client_id,
                                                         focus=False)
    
    def delete(self, *args):
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ self.var['name'].get() +" "+self.var['first_name'].get()+"\" ?"):
            self.farm.sales.client.delete_entry(i=self.client_id)
            
            self.master.left_frame.client_list_frame.refresh()
            self.master.refresh_right_frame()