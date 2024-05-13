# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

from ...farm import Farm

# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from ..widget import ComboboxDict

from tkinter.colorchooser import askcolor

# ne laisser que "extra" dans bakery_product
# on gère les batch dans une liste dynamique
# créer un objet farm.bakery.batch (cuissons)
# on y met id, name, code, position
# puis on répercute la liste ici
# avec un autre objet farm.bakery.process (accessible dans Produits)
# on y met id, bakery_product_id, bakery_dough_id, bakery_batch_id


# on pourra calculer (dans préparation)
# les erreurs
# les formats nécessaires
# les recettes détaillées

# dans gui sales commandes, on peut éditer 
# les feuilles de livraison (dont marché)

class ProductFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.PanedWindow.__init__(self, master, orient='horizontal')
        
        self.master = master
        self.farm = farm
        
        self.product_list_frame = ProductListFrame(master=self, 
                                          farm=self.farm)
        self.product_list_frame.grid(row=0, column=0, sticky='nw')
        
        self.edit_frame = None
    
    def init_edit_frame(self, logistic_goods_id):
        if self.edit_frame is not None:
            self.edit_frame.destroy()
        
        self.edit_frame = EditFrame(master=self, 
                                    farm=self.farm, 
                                    logistic_goods_id=logistic_goods_id)
        self.edit_frame.grid(row=0, column=1, sticky='nw')
        
class ProductListFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        self.farm = farm
        ttk.Frame.__init__(self, master)
    
        # product LIST
        # define columns
        columns = ('code', 'position')
        
        self.product_tree = ttk.Treeview(self, 
                                         columns=columns, 
                                         show='headings', 
                                         selectmode="browse",
                                         height=22)
        
        # define headings
        self.product_tree.heading('code', text='code', anchor=tk.W)
        self.product_tree.heading('position', text='#', anchor=tk.E)
        
        self.product_tree.column('code', width=100)
        self.product_tree.column('position', width=30, anchor=tk.E)
        
        self.fill()
        
        self.product_tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.product_tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='wns')
    
        self.insert_frame = NewProductFrame(master=self, 
                                            farm=self.farm)
        self.insert_frame.grid(row=1, column=0, columnspan=2)
    
    def fill(self):
        product = self.farm.logistic.goods.get_entries_from_sector(
            columns=['id', 'code', 'position'],
            sector='bakery',
            io='output',
            order_by='position DESC, code')
        for g in product:
            self.product_tree.insert('', tk.END, g[0], values=g[1:])
    
    def refresh(self, logistic_goods_id=None):
        self.product_tree.delete(*self.product_tree.get_children())
        self.fill()
        
        if self.master.edit_frame is not None:
            self.master.edit_frame.destroy()
        
        if logistic_goods_id is not None:
            self.product_tree.focus(logistic_goods_id)
            self.product_tree.selection_set(logistic_goods_id)
        
    def on_select(self, event):
        logistic_goods_id = self.product_tree.focus()
        if len(logistic_goods_id) > 0:
            print("you clicked on product id", logistic_goods_id)
            
            self.master.init_edit_frame(logistic_goods_id=logistic_goods_id)
            

class NewProductFrame(ttk.LabelFrame):
    def __init__(self, master, farm:Farm):
        
        self.farm = farm
        ttk.LabelFrame.__init__(self, master, text='Nouveau Produit')
    
        label_nom = ttk.Label(self, text="code")
        label_nom.grid(sticky="W",row=0,column=0, padx=2)
        
        self.new_code_value = tk.StringVar()
        
        entry_nom = ttk.Entry(self, width=10, 
                              textvariable=self.new_code_value)
        entry_nom.grid(sticky="W",row=1,column=0, padx=2, pady=2)
        
        button1 = ttk.Button(self, text = "Créer", command=self.insert)
        button1.grid(sticky="W",row=1,column=1, padx=2, pady=2)
    
    def insert(self):
        iid = self.farm.bakery.product.create(
            name = self.new_code_value.get(),
            code = self.new_code_value.get())
        
        self.master.refresh(logistic_goods_id=iid)
        
        self.new_code_value.set('')

class EditFrame(ttk.Frame):
    def __init__(self, master, farm, logistic_goods_id):
        self.farm = farm
        self.logistic_goods_id = logistic_goods_id
        
        ttk.Frame.__init__(self, master)
        
        label_nom = ttk.Label(self, text="nom")
        label_nom.grid(sticky="W",row=1,column=0)
        label_code = ttk.Label(self, text="code")
        label_code.grid(sticky="W",row=2,column=0)
        label_unit = ttk.Label(self, text="unité")
        label_unit.grid(sticky="W",row=3,column=0)
        label_unit = ttk.Label(self, text="format")
        label_unit.grid(sticky="W",row=4,column=0)
        label_color = ttk.Label(self, text="couleur")
        label_color.grid(sticky="W",row=5,column=0)
        label_position = ttk.Label(self, text="#")
        label_position.grid(sticky="W",row=6,column=0)
        
        # logistic goods
        data_logistic_goods = self.farm.logistic.goods.get_entry(i=self.logistic_goods_id)
        
        
        data_bakery_product = self.farm.bakery.product.get_entry_by_logistic_goods_id(i=self.logistic_goods_id,
                                                                               force=True)
        self.bakery_product_id = data_bakery_product['id']
        
        # populate processes if necessary
        # self.farm.bakery.product.populate_process(self.bakery_product_id)
        
        # get processes
        # list_data_bakery_process = self.farm.bakery.process.get_entries_by_bakery_product_id(self.bakery_product_id)
        
        self.edit_name_value = tk.StringVar()
        self.edit_code_value = tk.StringVar()
        self.edit_unit_value = tk.StringVar()
        self.edit_color_value = tk.StringVar()
        self.edit_position_value = tk.DoubleVar()
        
        self.edit_name_value.set(data_logistic_goods['name'])
        self.edit_code_value.set(data_logistic_goods['code'])
        self.edit_unit_value.set(data_logistic_goods['unit'])
        self.edit_color_value.set(data_logistic_goods['color'])
        self.edit_position_value.set(data_logistic_goods['position'])
        
        
        
        entry_nom = ttk.Entry(self, width=20, 
                             textvariable=self.edit_name_value)
        entry_nom.grid(sticky="W",row=1,column=1, columnspan=2, pady=2)
        entry_nom.bind('<Return>', 
                self.save)
        entry_nom.bind('<FocusOut>', 
                self.save)
        
        entry_code = ttk.Entry(self, width=12, 
                             textvariable=self.edit_code_value)
        entry_code.grid(sticky="W",row=2,column=1, columnspan=2, pady=2)
        entry_code.bind('<Return>', 
                self.save_and_refresh)
        entry_code.bind('<FocusOut>', 
                self.save_and_refresh)
        
        entry_unit = ttk.Entry(self, width=5, 
                             textvariable=self.edit_unit_value)
        entry_unit.grid(sticky="W",row=3,column=1, columnspan=2, pady=2)
        entry_unit.bind('<Return>', 
                self.save)
        entry_unit.bind('<FocusOut>', 
                self.save)
        
        # shapes combo box
        shapes = self.farm.bakery.shape.get_entries(order_by="position DESC, name")
        v = {s[1] : s[0] for s in shapes}
        self.edit_shape_cb = ComboboxDict(self,
                                           width=20,
                                           state="readonly",
                                           values=v,
                                           none_value='')
        self.edit_shape_cb.grid(sticky="w", row=4, column=1, columnspan=2, pady=2)
        self.edit_shape_cb.set_id(data_bakery_product['bakery_shape_id'])
        
        self.edit_shape_cb.bind("<<ComboboxSelected>>", 
                                self.save)
        
        entry_color = ttk.Entry(self, width=7,
                                textvariable=self.edit_color_value)
        entry_color.grid(sticky="w", row=5, column=1, pady=2)
        entry_color.bind('<Return>', 
                self.save)
        entry_color.bind('<FocusOut>', 
                self.save)
        ttk.Button(self, text="<", width=2, command=self.color_picker)\
            .grid(sticky="w", row=5, column=2, pady=2)
        
        entry_position = ttk.Entry(self, width=5, 
                             textvariable=self.edit_position_value)
        entry_position.grid(sticky="W",row=6, column=1, pady=2)
        entry_position.bind('<Return>', 
                self.save_and_refresh)
        entry_position.bind('<FocusOut>', 
                self.save_and_refresh)
        
        
        # Separator
        separator = ttk.Separator(self)
        separator.grid(row=7, column=0, padx=(20, 10), pady=10, sticky="ew", columnspan=3)
        
        # weight
        self.edit_weight_value = tk.DoubleVar()
        self.edit_weight_value.set(data_bakery_product['weight'])
        ttk.Label(self, text="poids")\
            .grid(row=8, column=0, sticky="w")
        entry_weight = ttk.Entry(self, width=5, textvariable=self.edit_weight_value)
        entry_weight.grid(row=8, column=1, columnspan=2, pady=2, sticky="w")
        entry_weight.bind('<Return>', 
                self.save)
        entry_weight.bind('<FocusOut>', 
                self.save)
        
        
        # batch edit
        self.edit_batch_combobox = {}
        
        processes = self.farm.bakery.process.get_entries(columns=['id',
                                                                  'bakery_batch_id',
                                                                 'bakery_dough_id'],
                                                         where='bakery_product_id = '+str(self.bakery_product_id),
                                                         list_dict=True)
        processes = {p['bakery_batch_id'] : p for p in processes}
        
        batches = self.farm.bakery.batch.get_entries(list_dict=True)
        for i, b in enumerate(batches):
            ttk.Label(self, text=b['code'])\
                .grid(row=9+i, column=0, sticky="w")
            
            self.edit_batch_combobox[b['id']] = self.batch_combobox(self)
            self.edit_batch_combobox[b['id']].grid(sticky="WE",row=8+i,column=1, columnspan=2, pady=2)
            if b['id'] in processes.keys():
                self.edit_batch_combobox[b['id']].set_id(processes[b['id']]['bakery_dough_id'])
        
        # label_extra = ttk.Label(self, text="extra")
        # label_extra.grid(sticky="W",row=8+len(batches),column=0, pady=2)
        
        # self.edit_extra_combobox = self.batch_combobox(self)
        # self.edit_extra_combobox.grid(sticky="WE",row=8+len(batches),column=1, columnspan=2)
        # self.edit_extra_combobox.set_id(data_bakery_product['extra_bakery_dough_id'])
        
        # button1 = ttk.Button(self, text = "Éditer", command=self.save)
        # button1.grid(sticky="W",row=8+len(batches)+0,column=0, pady=2)
        
        button2 = ttk.Button(self, text = "Supprimer", command=self.remove)
        button2.grid(sticky="e",row=9+len(batches)+1,column=2, pady=2)
    
    def color_picker(self, *event):
        current_color = self.edit_color_value.get()
        
        if current_color == '':
            current_color = '#ffffff'
        
        colors = askcolor(title="Sélectionner une couleur",
                          color=current_color)
        
        if colors[1] is not None:
            self.edit_color_value.set(colors[1])
        
        self.save()
    
    def batch_combobox(self, master):
        dough = self.farm.bakery.dough.get_entries(order_by="name")
        
        values = {d[1] : d[0] for d in dough}
                
        cb= ComboboxDict(master, 
                  width=20, 
                  state="readonly",
                  none_value='',
                  values=values)
        
        cb.bind("<<ComboboxSelected>>", 
                self.save)
        
        return cb
    
    def save_and_refresh(self, *event):
        self.save()
        self.master.product_list_frame.refresh(logistic_goods_id=self.logistic_goods_id)
    
    def save(self, *event):
        self.farm.logistic.goods.update_entry(
            i = self.logistic_goods_id,
            name = self.edit_name_value.get(),
            code = self.edit_code_value.get(),
            unit = self.edit_unit_value.get(),
            position = self.edit_position_value.get())
        
        self.farm.bakery.product.update_entry(
            i=self.bakery_product_id,
            weight = self.edit_weight_value.get(),
            bakery_shape_id=self.edit_shape_cb.get_id())
            # extra_bakery_dough_id=self.edit_extra_combobox.get_id())
        
        processes = self.farm.bakery.process.get_entries(columns=['id',
                                                                  'bakery_batch_id',
                                                                 'bakery_dough_id'],
                                                         where='bakery_product_id = '+str(self.bakery_product_id),
                                                         list_dict=True)
        processes = {p['bakery_batch_id'] : p for p in processes}
        
        for bakery_batch_id, ebcb in self.edit_batch_combobox.items():
            if bakery_batch_id in processes.keys():
                if ebcb.get_id() is None:
                    self.farm.bakery.process.delete_entry(
                        i = processes[bakery_batch_id]['id'])
                else:
                    self.farm.bakery.process.update_entry(
                        i = processes[bakery_batch_id]['id'],
                        bakery_dough_id = ebcb.get_id())
            else:
                if ebcb.get_id() is not None:
                    self.farm.bakery.process.insert_entry(
                        bakery_product_id = self.bakery_product_id,
                        bakery_batch_id = bakery_batch_id,
                        bakery_dough_id = ebcb.get_id())
        
        
    def remove(self):
        
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ self.edit_code_value.get() +"\" ?"):
            self.farm.logistic.goods.delete_entry(i=self.logistic_goods_id)
            self.master.product_list_frame.refresh()
        
    
