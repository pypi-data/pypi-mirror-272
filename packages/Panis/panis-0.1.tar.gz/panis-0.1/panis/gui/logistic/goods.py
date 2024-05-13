# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from ...farm import Farm

from tkinter.colorchooser import askcolor

# TODO : make trigger automatic according logistic_goods columns

class GoodsPW(ttk.PanedWindow):
    def __init__(self, master, farm:Farm):
        
        ttk.PanedWindow.__init__(self, master, orient='horizontal')
        
        self.master = master
        self.farm = farm
        
        self.create_left_pane()
        self.create_right_pane()
    
    def create_left_pane(self):
        
        left_pane = tk.Frame(self, width=20, height=600)
        self.add(left_pane)
        
        # GOODS LIST
        # define columns
        columns = ('name')
        
        self.goods_tree = ttk.Treeview(left_pane, 
                                       columns=columns,
                                       show='headings', 
                                       selectmode="browse",
                                       height=22)
        
        # define headings
        self.goods_tree.heading('name', text='nom', anchor=tk.W)
        
        self.goods_tree.column('name', width=200)
        
        self.fill_goods_tree()
        
        self.goods_tree.bind('<<TreeviewSelect>>', self.on_goods_tree_select)
        
        self.goods_tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(left_pane, orient=tk.VERTICAL, command=self.goods_tree.yview)
        self.goods_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
    
        self.create_new_frame(master=left_pane)
    
    def fill_goods_tree(self):
        goods = self.farm.logistic.goods.get_entries(columns=['id','name'], 
                                                     order_by='name',
                                                     where="io<>'output'")
        
        for g in goods:
            self.goods_tree.insert('', tk.END, g[0], values=g[1:])
    
    def refresh_goods_tree(self, item_id=None):
        self.goods_tree.delete(*self.goods_tree.get_children())
        self.fill_goods_tree()
        
        if item_id is not None:
            self.goods_tree.focus(item_id)
            self.goods_tree.selection_set(item_id)
        else:
            self.edit_id_value.set(-1)
            self.edit_name_value.set('')
            self.edit_code_value.set('')
            self.edit_unit_value.set('')
            self.edit_position_value.set(0)
            self.edit_io_value.set('input')
            self.edit_trigger_bakery_value.set(0)
            self.edit_trigger_mill_value.set(0)
        
    def on_goods_tree_select(self, event):
        id_goods = self.goods_tree.focus()
        if len(id_goods) > 0:
            print("you clicked on goods id", id_goods)
            
            data = self.farm.logistic.goods.get_entry(i=id_goods)
            
            self.edit_id_value.set(id_goods)
            self.edit_name_value.set(data['name'])
            # self.edit_code_value.set(data['code'])
            # self.edit_unit_value.set(data['unit'])
            # self.edit_color_value.set(data['color'])
            self.edit_position_value.set(data['position'])
            # self.edit_io_value.set(data['io'])
            # self.edit_trigger_bakery_value.set(data['trigger_bakery'])
            # self.edit_trigger_mill_value.set(data['trigger_mill'])
    
    def create_new_frame(self, master):
        new_frame = tk.LabelFrame(master, width=200, height=200, text="Nouveau", padx=5, pady=5)
        new_frame.grid(row=1, column=0, sticky='ew', columnspan=2)
        
        label_nom = ttk.Label(new_frame, text="nom")
        label_nom.grid(sticky="W",row=0,column=0)
        
        self.new_name_value = tk.StringVar()
        
        entry_nom = ttk.Entry(new_frame, width=20, 
                             textvariable=self.new_name_value)
        entry_nom.grid(sticky="W",row=1,column=0)
        
        button1 = ttk.Button(new_frame, text = "Créer", command=self.new_goods)
        button1.grid(sticky="W",row=1,column=1)
        
    def create_right_pane(self):
        # GOODS EDITOR
        self.right_pane = tk.Frame(self, width=200)
        self.add(self.right_pane)
        
        self.create_edit_frame()
        
    def create_edit_frame(self):
        edit_frame = tk.LabelFrame(self.right_pane, width=200, height=200, text="Éditer", padx=5, pady=5)
        edit_frame.grid(row=0, column=0, sticky='ew')
        
        label_nom = ttk.Label(edit_frame, text="nom")
        label_nom.grid(sticky="W",row=1,column=0)
        # label_nom = ttk.Label(edit_frame, text="code")
        # label_nom.grid(sticky="W",row=2,column=0)
        # label_unit = ttk.Label(edit_frame, text="unité")
        # label_unit.grid(sticky="W",row=3,column=0)
        # label_color = ttk.Label(edit_frame, text="couleur")
        # label_color.grid(sticky="W",row=4,column=0)
        label_position = ttk.Label(edit_frame, text="#")
        label_position.grid(sticky="W",row=5,column=0)
        
        self.edit_id_value = tk.IntVar()
        self.edit_id_value.set(-1)
        self.edit_name_value = tk.StringVar()
        # self.edit_code_value = tk.StringVar()
        # self.edit_unit_value = tk.StringVar()
        self.edit_position_value = tk.DoubleVar()
        # self.edit_color_value = tk.StringVar()
        
        entry_nom = ttk.Entry(edit_frame, width=20, 
                             textvariable=self.edit_name_value)
        entry_nom.grid(sticky="W",row=1,column=1, columnspan=2, pady=2)
        entry_nom.bind('<Return>', 
                self.save_and_refresh)
        entry_nom.bind('<FocusOut>', 
                self.save_and_refresh)
        
        # entry_code = ttk.Entry(edit_frame, width=20, 
                             # textvariable=self.edit_code_value)
        # entry_code.grid(sticky="W",row=2,column=1, columnspan=2, pady=2)
        
        # entry_unit = ttk.Entry(edit_frame, width=5, 
                             # textvariable=self.edit_unit_value)
        # entry_unit.grid(sticky="W",row=3,column=1, columnspan=2, pady=2)
        
        # entry_color = ttk.Entry(edit_frame, width=7,
                                # textvariable=self.edit_color_value)
        # entry_color.grid(sticky="w", row=4, column=1, pady=2)
        # ttk.Button(edit_frame, text="<", width=2, command=self.color_picker)\
            # .grid(sticky="w", row=4, column=2, pady=2)
        
        entry_position = ttk.Entry(edit_frame, width=5, 
                              textvariable=self.edit_position_value)
        entry_position.grid(sticky="W",row=5,column=1, columnspan=2, pady=2)
        entry_position.bind('<Return>', 
                self.save_and_refresh)
        entry_position.bind('<FocusOut>', 
                self.save_and_refresh)
        
        # self.edit_trigger_bakery_value = tk.BooleanVar()
        # self.edit_trigger_mill_value = tk.BooleanVar()
        
        # ttk.Checkbutton(edit_frame, text="Boulange", variable=self.edit_trigger_bakery_value).grid(sticky="w", row=6, column=0, columnspan=2, pady=2)
        # ttk.Checkbutton(edit_frame, text="Meunerie", variable=self.edit_trigger_mill_value).grid(sticky="w", row=7, column=0, columnspan=2, pady=2)
        
        # self.edit_io_value = tk.StringVar()
        
        # radio_1 = ttk.Radiobutton(edit_frame, text="intrant", variable=self.edit_io_value, value='input')
        # radio_1.grid(sticky="w", row=8, column=0, pady=2)
        # radio_2 = ttk.Radiobutton(edit_frame, text="prod.", variable=self.edit_io_value, value='output')
        # radio_2.grid(sticky="w", row=8, column=1, pady=2)
        # radio_3 = ttk.Radiobutton(edit_frame, text="les deux", variable=self.edit_io_value, value='both')
        # radio_3.grid(sticky="w", row=8, column=2, pady=2)
        
        # button1 = ttk.Button(edit_frame, text = "Éditer", command=self.edit_goods)
        # button1.grid(sticky="W",row=9,column=0, pady=2)
        
        button2 = ttk.Button(edit_frame, text = "Supprimer", command=self.remove_goods)
        button2.grid(sticky="e",row=9,column=2, pady=2)
    
    def color_picker(self, *event):
        current_color = self.edit_color_value.get()
        
        if current_color == '':
            current_color = '#ffffff'
        
        colors = askcolor(title="Sélectionner une couleur",
                          color=current_color)
        
        if colors[1] is not None:
            self.edit_color_value.set(colors[1])
    
    def save(self, *event):
        self.farm.logistic.goods.update_entry(
                            i= self.edit_id_value.get(),
                            name = self.edit_name_value.get(),
                            position = self.edit_position_value.get(),
                            )
    
    def save_and_refresh(self, *event):
        self.save()
        self.refresh_goods_tree(self.edit_id_value.get())
    
    def remove_goods(self):
        
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ self.edit_name_value.get() +"\" ?"):
            self.farm.logistic.goods.delete_entry(i=self.edit_id_value.get())
            self.refresh_goods_tree()
        
    
        
    def new_goods(self):
        
        iid = self.farm.logistic.goods.insert_entry(name = self.new_name_value.get())
        
        self.refresh_goods_tree(item_id=iid)
        
        self.new_name_value.set('')
