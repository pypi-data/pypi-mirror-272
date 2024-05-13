# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

# import os
# import sys

from ...farm import Farm

# from gui.widget import ComboboxDict
# from gui.widget import ScrollbarFrame
# from gui.widget import ValueEntry

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ..widget import ComboboxDict, ScrollbarFrame, ValueEntry

import numpy as np

class DoughRecipeFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.dough_frame = DoughFrame(master=self, 
                                      farm=self.farm)
        self.dough_frame.grid(row=0, column=0, sticky='nw')
        self.edit_frame = None
        
    def init_edit_frame(self, dough_id):
        if self.edit_frame is not None:
            self.edit_frame.destroy()
        
        self.edit_frame = EditFrame(master=self, 
                                    farm=self.farm, 
                                    dough_id=dough_id)
        self.edit_frame.grid(row=0, column=1, sticky='nw', padx=10)

class DoughFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master, width=20, height=600)
        self.farm = farm
        
        
        
        # RECIPE LIST
        # define columns
        columns = ('name', 'position')
        
        self.tree = ttk.Treeview(self, 
                                 columns=columns, 
                                 show='headings', 
                                 selectmode="browse",
                                 height=22)
        
        # define headings
        self.tree.heading('name', text='nom', anchor=tk.W)
        self.tree.heading('position', text='#', anchor=tk.E)
        
        self.tree.column('name', width=170)
        self.tree.column('position', width=30, anchor=tk.E)
        
        self.fill_tree()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
        
        self.create_new_frame = NewDoughFrame(master=self, 
                                              farm=self.farm)
        self.create_new_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    
    def fill_tree(self):
        dough = self.farm.bakery.dough.get_entries(columns=['id','name', 'position'], 
                                                     order_by='position DESC, name')
        
        for g in dough:
            self.tree.insert('', tk.END, g[0], values=g[1:])
    
    def refresh(self, item_id=None, destroy_edit_frame=True):
        self.tree.delete(*self.tree.get_children())
        self.fill_tree()
        
        if self.master.edit_frame is not None and destroy_edit_frame:
            self.master.edit_frame.destroy()
        
        if item_id is not None:
            if destroy_edit_frame:
                self.tree.focus(item_id)
            self.tree.selection_set(item_id)
        
    def on_tree_select(self, event):
        dough_id = self.tree.focus()
        if len(dough_id) > 0:
            
            self.master.init_edit_frame(dough_id=dough_id)

class NewDoughFrame(ttk.LabelFrame):
    def __init__(self, master, farm:Farm):
        
        ttk.LabelFrame.__init__(self, master, text="Nouvelle Recette")
        self.farm = farm
        
        label_nom = ttk.Label(self, text="nom")
        label_nom.grid(sticky="W",row=0,column=0)
        
        self.new_dough_name_value = tk.StringVar()
        
        entry_name = ttk.Entry(self, width=20, 
                             textvariable=self.new_dough_name_value)
        entry_name.grid(sticky="W",row=1,column=0)
        
        button1 = ttk.Button(self, text = "Créer", command=self.insert)
        button1.grid(sticky="W",row=1,column=1)
        
    def insert(self, *args):
        iid = self.farm.bakery.dough.insert_entry(name = self.new_dough_name_value.get())
        
        self.master.refresh(item_id=iid)
        
        self.new_dough_name_value.set('')

class EditFrame(ttk.Frame):
    
    def __init__(self, master, farm, dough_id):
        ttk.Frame.__init__(self, master, width=400)
        
        self.master = master
        self.farm = farm
        self.dough_id = dough_id
        
        self.edit_dough_frame = EditDoughFrame(master=self, 
                                               farm=self.farm, 
                                               dough_id=dough_id)
        self.edit_dough_frame.grid(row=0, column=0, sticky='ew')
        
        self.recipe_frame = RecipeFrame(master=self, 
                                        farm=self.farm, 
                                        dough_id=self.dough_id)
        self.recipe_frame.grid(row=1, column=0, sticky='ew')
        
        # button1 = ttk.Button(self, text = "Enregistrer les modifications", command=self.save)
        # button1.grid(sticky="W",row=2,column=0)
        
        button2 = ttk.Button(self, text = "Supprimer cette recette", command=self.delete)
        button2.grid(sticky="e",row=3,column=0, pady=20, padx=30)
    
    def save(self, *args):
        
        self.edit_dough_frame.save()
        self.recipe_frame.save()
        
        self.master.dough_frame.refresh(self.dough_id)
    
    def delete(self):
        data = self.farm.bakery.dough.get_entry(i=self.dough_id, columns=['name'])
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ data['name'] +"\" ?"):
            self.farm.bakery.dough.delete_entry(i=self.dough_id)
            self.master.dough_frame.refresh()
    

class EditDoughFrame(ttk.Frame):
    def __init__(self, master, farm, dough_id):
        ttk.Frame.__init__(self, master)
        self.dough_id = dough_id
        self.farm = farm
        
        label_nom = ttk.Label(self, text="nom")
        label_nom.grid(sticky="W",row=0,column=0, padx=5)
        label_position = ttk.Label(self, text="#")
        label_position.grid(sticky="W",row=1,column=0, padx=5)
        label_bwli = ttk.Label(self, text="cru / cuit")
        label_bwli.grid(sticky="W",row=2,column=0, padx=5)
        label_ed = ttk.Label(self, text="rab")
        label_ed.grid(sticky="W",row=3,column=0, padx=5)
        
        data = self.farm.bakery.dough.get_entry(i=dough_id)
        
        self.edit_dough_data = {}
        self.edit_dough_data['name'] = tk.StringVar(value=data['name'])
        self.edit_dough_data['baking_weight_loss_inverse'] = tk.DoubleVar(value=data['baking_weight_loss_inverse'])
        self.edit_dough_data['position'] = tk.DoubleVar(value=data['position'])
        self.edit_dough_data['sourdough'] = tk.BooleanVar(value=data['sourdough'])
        self.edit_dough_data['old_sourdough'] = tk.BooleanVar(value=data['old_sourdough'])
        self.edit_dough_data['king_sourdough_weight'] = tk.StringVar(value=data['king_sourdough_weight'])
        self.edit_dough_data['extra_dough'] = tk.DoubleVar(value=data['extra_dough']*100)
        
        entry_name = ttk.Entry(self, width=20, 
                             textvariable=self.edit_dough_data['name'])
        entry_name.grid(sticky="W",row=0,column=1, columnspan=2, pady=2, padx=5)
        entry_name.bind('<Return>', 
                self.save_and_refresh)
        entry_name.bind('<FocusOut>', 
                self.save_and_refresh)
        
        entry_position = ttk.Entry(self, width=5, 
                             textvariable=self.edit_dough_data['position'])
        entry_position.grid(sticky="W",row=1,column=1, columnspan=2, pady=2, padx=5)
        entry_position.bind('<Return>', 
                self.save_and_refresh)
        entry_position.bind('<FocusOut>', 
                self.save_and_refresh)
        
        entry_bwli = ttk.Entry(self, width=5, 
                             textvariable=self.edit_dough_data['baking_weight_loss_inverse'])
        entry_bwli.grid(sticky="W",row=2,column=1, columnspan=2, pady=2, padx=5)
        entry_bwli.bind('<Return>', 
                self.save)
        entry_bwli.bind('<FocusOut>', 
                self.save)
        
        entry_ed = ttk.Entry(self, width=5, 
                             textvariable=self.edit_dough_data['extra_dough'])
        entry_ed.grid(sticky="W",row=3,column=1, columnspan=1, pady=2, padx=5)
        entry_ed.bind('<Return>', 
                self.save)
        entry_ed.bind('<FocusOut>', 
                self.save)
        ttk.Label(self, text="%").grid(row=3, column=2, pady=2, padx=0, sticky="w")
        
        ttk.Checkbutton(self, text="C'est un levain", variable=self.edit_dough_data['sourdough'],
                        command=self.on_sourdough_check)\
            .grid(sticky="w", row=4, column=0, columnspan=3, pady=2, padx=5)
        
        # self.check_old_sourdough = ttk.Checkbutton(self, text="Utiliser du vieux levain", variable=self.edit_dough_data['old_sourdough'],
                        # command=self.save,
                        # command=self.on_sourdough_check)
        # self.check_old_sourdough.grid(sticky="w", row=5, column=0, columnspan=3, pady=2, padx=5)
        
        self.label_king_sourdough = ttk.Label(self, text="Poids de levain chef")
        self.entry_king_sourdough = ValueEntry(self, width=5, 
                             textvariable=self.edit_dough_data['king_sourdough_weight'])
        self.label_king_sourdough_unit = ttk.Label(self, text="kg")
        
        self.entry_king_sourdough.bind('<Return>', 
                self.save)
        self.entry_king_sourdough.bind('<FocusOut>', 
                self.save)
        
        self.on_sourdough_check()
    
    def on_sourdough_check(self, **kwargs):
        # if self.edit_dough_data['sourdough'].get():
            # self.check_old_sourdough.configure(state='disabled')
            # self.edit_dough_data['old_sourdough'].set(True)
        # else:
            # self.check_old_sourdough.configure(state='normal')
        
        if self.edit_dough_data['sourdough'].get():
            self.label_king_sourdough.grid(sticky="w", row=6, column=0, columnspan=2, pady=2, padx=5)
            self.entry_king_sourdough.grid(sticky="e",row=6,column=2, pady=2, padx=(5,2))
            self.label_king_sourdough_unit.grid(sticky="w", row=6, column=3, pady=2, padx=2)
        else:
            self.label_king_sourdough.grid_forget()
            self.entry_king_sourdough.grid_forget()
            self.label_king_sourdough_unit.grid_forget()
        
        self.save()
    
    def save(self, *args):
        self.farm.bakery.dough.update_entry(
                            i= self.dough_id,
                            name = self.edit_dough_data['name'].get(),
                            baking_weight_loss_inverse = self.edit_dough_data['baking_weight_loss_inverse'].get(),
                            sourdough = int(self.edit_dough_data['sourdough'].get()),
                            old_sourdough = int(self.edit_dough_data['old_sourdough'].get()),
                            position = self.edit_dough_data['position'].get(),
                            king_sourdough_weight = self.edit_dough_data['king_sourdough_weight'].get(),
                            extra_dough = self.edit_dough_data['extra_dough'].get()/100
                            )
    
    def save_and_refresh(self, *args):
        self.save()
        self.master.master.dough_frame.refresh(item_id=self.dough_id,
                                               destroy_edit_frame=False)
        
class RecipeFrame(ttk.Frame):
    def __init__(self, master, farm, dough_id):
        self.master = master
        self.farm = farm
        self.dough_id = dough_id
        
        ttk.Frame.__init__(self, master)
        
        # Create a ScrolledFrame widget
        self.box = ScrollbarFrame(self, text="Ingrédients", height=300, width=370)
        self.box.grid(row=0, column=0, sticky='ewns', columnspan=2, padx=5, pady=5)

        self.fill_ingredients()
        
        self.new_recipe_goods_combobox = self.combobox_ingredient(self)
        self.new_recipe_goods_combobox.grid(row=1, column=0, sticky="we", pady=5, padx=5)
        
        but = ttk.Button(self, text = "ajouter l'ingrédient", command=self.add)
        but.grid(sticky="e",row=1,column=1)
        
    def fill_ingredients(self):
        self.ingredients_tk_objects = []
        
        self.percent_labels = {}
        
        ingredients_logistic = self.farm.bakery.recipe.get_logistic_goods(bakery_dough_id=self.dough_id)
        self.ingredients_quantity_var = {}
        for row_i, ing in enumerate(ingredients_logistic):
            self._display_ingredient(row_i = row_i,
                                     iid=ing['id'],
                                     name=ing['logistic_goods_name'], 
                                     quantity=ing['quantity'], 
                                     unit=ing['logistic_goods_unit'])
        
        ingredients_dough = self.farm.bakery.recipe.get_bakery_dough(bakery_dough_id=self.dough_id)
        for row_i, ing in enumerate(ingredients_dough):
            self._display_ingredient(row_i = len(ingredients_logistic) + row_i,
                                     iid=ing['id'],
                                     name=ing['bakery_dough_name'], 
                                     quantity=ing['quantity'], 
                                     unit='kg')
            
        self._refresh_percent()
        
    def _display_ingredient(self, row_i, iid, name, quantity, unit):
        label_name = ttk.Label(self.box.scrolled_frame, text=name, width=25)
        label_name.grid(row=row_i, column=0, sticky='w', padx=5)
        
        self.ingredients_quantity_var[iid] = tk.DoubleVar()
        self.ingredients_quantity_var[iid].set(quantity)
        
        quantity = ValueEntry(self.box.scrolled_frame, width=7, 
                             textvariable=self.ingredients_quantity_var[iid])
        quantity.grid(row=row_i, column=1, padx=2, pady=2)
        
        quantity.bind('<Return>', 
                self.save)
        quantity.bind('<FocusOut>', 
                self.save)
        
        unit = ttk.Label(self.box.scrolled_frame, text=unit)
        unit.grid(row=row_i, column=2, sticky='w', padx=2)
        
        percent_label = ttk.Label(self.box.scrolled_frame, text='100.00 %', width=8, anchor='e')
        percent_label.grid(row=row_i, column=3, sticky='e', padx=2)
        self.percent_labels[iid] = percent_label
        
        delete = ttk.Label(self.box.scrolled_frame, text="X", anchor="center", width=5)
        delete.grid(row=row_i, column=4, sticky='w', padx=2)
        delete.bind("<Button-1>", lambda event, i=iid, name=name : self.delete(i, name))
        
        self.ingredients_tk_objects += [label_name, quantity, unit, percent_label, delete]
    
    def _refresh_percent(self):
        q_tot = np.sum([iqv.get() for iqv in self.ingredients_quantity_var.values()])
        
        for iid, pl in self.percent_labels.items():
            percent = self.ingredients_quantity_var[iid].get() / q_tot * 100
            percent = '{:.2f}'.format(round(percent, 2))
            pl.configure(text=str(percent)+' %')
    
    def refresh(self):
        for obj in self.ingredients_tk_objects:
            obj.destroy()
        self.fill_ingredients()
        
    def combobox_ingredient(self, master):
        ingredient_logistic_goods = self.farm.logistic.goods.get_entries_from_sector(
            columns=['id', 'name'],
            sector='bakery',
            io='input',
            order_by='name')
        
        ingredient_bakery_recipe = self.farm.bakery.dough.get_entries(
            columns=['id', 'name'])
        
        
        values_logistic = {ing[1] : ('logistic_goods', ing[0]) for ing in ingredient_logistic_goods}
        
        values_recipe = {ing[1] : ('bakery_dough', ing[0]) for ing in ingredient_bakery_recipe}
        
        values = {'' : (None, None),
                  '===Ingrédients===' : (None, None),
                  **values_logistic,
                  ' ' : None,
                  '===Recettes===' : (None, None),
                  **values_recipe}
        
        cb= ComboboxDict(
                  master, 
                  width=20, 
                  state="readonly",
                  values=values)
        
        return cb
    
    def add(self, *args):
        self.save()
        
        table_name, item_id = self.new_recipe_goods_combobox.get_id()
        
        if table_name is not None:
            if table_name == 'logistic_goods':
                self.farm.bakery.recipe.insert_entry(
                    bakery_dough_id = self.dough_id,
                    logistic_goods_id = item_id)
            if table_name == 'bakery_dough':
                self.farm.bakery.recipe.insert_entry(
                    bakery_dough_id = self.dough_id,
                    bakery_dough_as_recipe_id = item_id)
        
        self.refresh()
        self.new_recipe_goods_combobox.set_id(None)

    def save(self, *args):
        self._refresh_percent()
        
        for i, quantity_var in self.ingredients_quantity_var.items():
            self.farm.bakery.recipe.update_entry(i = i,
                                                 quantity = quantity_var.get())
    
    def delete(self, i, name):
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ name +"\" ?"):
            self.farm.bakery.recipe.delete_entry(i=i)
            self.refresh()
            
