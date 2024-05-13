# -*- coding: utf-8 -*-

import os
# import sys

import shutil

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile

from ..farm import Farm

from . import cooperation
from . import logistic
from . import bakery
from . import sales

from pathlib import Path

from ttkthemes import ThemedTk

modules = [
            # {'title':'Coopération',
            # 'id':'cooperation',
            # 'submodules':[{'title':'Réunions',
            #               'id':'meetingsubject',
            #               'tkwidget':cooperation.MeetingSubjectFrame
            #               }
            #              ]
            # },
            {'title':'Logistique',
             'id':'logistic',
             'submodules':[{'title':'Ingrédients',
                           'id':'logistic_goods',
                           'tkwidget':logistic.GoodsPW
                           },
                           # {'title':'Stocks',
                           #  'id':'logistic_stocks'
                           # }
                          ]
             },
            {'title':'Boulangerie',
            'id':'bakery',
            'submodules':[
                        # {'title':'Paramètres',
                        #    'id':'bakery_parameter',
                        #    'tkwidget':bakery.ParameterFrame
                        #    },
                          {'title':'Recettes',
                           'id':'bakery_recipe',
                           'tkwidget':bakery.DoughRecipeFrame
                           },
                          {'title':'Cuissons',
                                         'id':'bakery_batch',
                                         'tkwidget':bakery.BatchFrame
                           },
                          {'title':'Formats',
                           'id':'bakery_shape',
                           'tkwidget':bakery.ShapeFrame
                           },
                          {'title':'Produits',
                           'id':'bakery_product',
                           'tkwidget':bakery.ProductFrame
                           },
                          {'title':'Allocation',
                           'id':'bakery_allocation',
                           'tkwidget':bakery.AllocationFrame
                           }
                          ]
            },
            {'title':'Commercialisation',
            'id':'sales',
            'submodules':[{'title':'Boulange',
                           'id':'sales_distribution',
                           'tkwidget':sales.DistributionFrame
                           },
                          {'title':'Livraisons',
                           'id':'sales_delivery',
                           'tkwidget':sales.DeliveryFrame
                           },
                          {'title':'Clients',
                           'id':'sales_client',
                           'tkwidget':sales.ClientFrame
                           },
                          {'title':'Commandes',
                           'id':'sales_order',
                           'tkwidget':sales.OrderFrame}
                          ]
            }
           ]


class MainWindow(ThemedTk):

    def __init__(self, modules):
        # tk.Tk.__init__(self)
        ThemedTk.__init__(self, theme="arc")
        
        # Import the tcl file
        # style_folder_path = Path(__file__).parent / "style"
        # style_file_path = str(style_folder_path / "forest-light.tcl")
        # self.tk.call('source', style_file_path)
        
        # Set the theme with the theme_use method
        self.style = ttk.Style()
        # self.style.theme_use('forest-light')
        self.style.configure('red.TLabel', foreground='red')
        self.style.configure('green.TLabel', foreground='green')
        self.style.configure('blue.TLabel', foreground='blue')
        # self.style.configure('disabled.TEntry', background='#cacaca')
        
        
        self.create_menu_bar()
        
        # self.geometry("1100x600")
        #getting screen width and height of display
        width= self.winfo_screenwidth() 
        height= self.winfo_screenheight()
        #setting tkinter window size
        self.geometry("%dx%d" % (width, height))
        
        self.title("Panis")
        self.option_add("*tearOff", False) # This redis always a good idea
        
        self.modules = modules
        
        self.farm = None
        self.content_PW = None
        
        # quit button
        self.protocol('WM_DELETE_WINDOW', self.exit_paille)
        
    def exit_paille(self):
        if self.farm is not None:
            print('closing farm...')
            self.farm.conn.close()
            
        self.destroy()
    
    # MENU BAR
    # ========
    
    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        self.menu_file = tk.Menu(menu_bar, tearoff=0)
        self.menu_file.add_command(label="Nouveau", command=self.new_file)
        self.menu_file.add_command(label="Ouvrir", command=self.open_file)
        self.menu_file.add_command(label="Enregistrer sous", command=self.save_as, state='disabled')
        self.menu_file.add_command(label="Fermer", command=self.close, state='disabled')
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.exit_paille)
        menu_bar.add_cascade(label="Fichier", menu=self.menu_file)

        # menu_edit = ttk.Menu(menu_bar, tearoff=0)
        # menu_edit.add_command(label="Undo", command=self.do_something)
        # menu_edit.add_separator()
        # menu_edit.add_command(label="Copy", command=self.do_something)
        # menu_edit.add_command(label="Cut", command=self.do_something)
        # menu_edit.add_command(label="Paste", command=self.do_something)
        # menu_bar.add_cascade(label="Edit", menu=menu_edit)

        menu_help = tk.Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="À propos", command=self.do_about)
        menu_bar.add_cascade(label="Aide", menu=menu_help)

        self.config(menu=menu_bar)

    def new_file(self):
        # bug sur cette fonction
        path = asksaveasfile(title="Create new file",
                               filetypes=[("sqlite database", ".db")])
        self.open_farm(path.name)
        
    def open_file(self):
        path = askopenfilename(title="Choose the file to open",
                               filetypes=[("sqlite database", ".db")])
        
        self.open_farm(path)
        
        
    def open_farm(self, path):
        self.close()
        
        print('opening', path)
        
        self.farm = Farm(path)
        print(self.farm)
        
        self.create_content_PW()
        
        self.menu_file.entryconfigure(2, state='normal')
        self.menu_file.entryconfigure(3, state='normal')
    
    def save_as(self):
        if self.farm is not None:
            path = asksaveasfile(title="Create new file",
                                 filetypes=[("sqlite database", ".db")])
            
            shutil.copyfile(self.farm.path, path.name)
            self.open_farm(path.name)
        
    def do_about(self):
        messagebox.showinfo("paille", "Gestionnaire Unique pour une Agriculture Nouvellement Organisée")
    
    def close(self):
        if self.farm is not None:
            self.farm.conn.close()
        
        if self.content_PW is not None:
            self.content_PW.destroy()
    
        self.menu_file.entryconfigure(2, state='disabled')
        self.menu_file.entryconfigure(3, state='disabled')
    
    # content_PW
    # =========
    def create_content_PW(self):
        self.content_PW = ttk.PanedWindow(self, orient="horizontal")
        # self.content_PW = ttk.Frame(self)
        # self.content_PW.grid(column=0, row=0, sticky='nsew')
        self.content_PW.pack(fill="both", expand=True)
        
        self.content_PW.grid_rowconfigure(0, weight=1)
        self.content_PW.grid_columnconfigure(0, weight=1)
        
        self.modules_tree_frame = ModulesTreeFrame(master=self.content_PW, 
                                             farm=self.farm,
                                             modules=self.modules)
        # self.modules_tree_frame.grid(row=0, column=0, sticky='wns')
        self.content_PW.add(self.modules_tree_frame)
        
        self.module_frame = ModuleFrame(master=self.content_PW, 
                                     farm=self.farm,
                                     modules=self.modules)
        # self.module_frame.grid(row=0, column=1, sticky='nswe', padx=5)
        self.content_PW.add(self.module_frame)
        
        self.modules_tree_frame.set_module_frame(self.module_frame)
        
    
class ModulesTreeFrame(ttk.Frame):
    def __init__(self, master, farm, modules, **args):
        
        ttk.Frame.__init__(self, master, **args)
        
        self.master = master
        self.farm = farm
        self.modules = modules
                
        file_name = ttk.Label(self, text=self.farm.file_name+'.db')
        file_name.grid(row=0, column=0, sticky='w', padx=5)
        
        # columns = ('module',)
        self.tree = ttk.Treeview(self,
                                 show='tree',
                                 selectmode="browse",
                                 height=20)
        # self.tree.column('module', width=20)
        
        self.insert_items(modules=self.modules)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)  
        self.tree.grid(row=1, column=0, sticky='wns')
        
    def insert_items(self, modules, master_id=''):
        for i, m in enumerate(modules):
                        
            # insert(master_id, index, id, options...)
            self.tree.insert(master_id, i, m['id'], 
                            text = m['title'])
            
            if 'submodules' in m.keys():
                self.insert_items(modules=m['submodules'], 
                                  master_id=m['id'])
    
    def on_tree_select(self, event):
        self.open_tree_item(self.tree.focus())
        
        self.module_frame.open_module(self.tree.focus())
        
    def open_tree_item(self, item_id):
        if self.tree.item(item_id, 'open') == 0:
            self.tree.item(item_id, open=True)
        else:
            self.tree.item(item_id, open=False)
    
    def set_module_frame(self, module_frame):
        self.module_frame = module_frame

class ModuleFrame(ttk.Frame):
    def __init__(self, master, farm, modules):
        
        ttk.Frame.__init__(self, master)
                
        self.master = master
        self.farm = farm
        self.modules = modules
    
        self.content = ttk.Frame(self)
        
        
    def open_module(self, module_id):
        
        m = get_module(modules=self.modules, 
                       iid=module_id)
        
        self.content.destroy()
        
        self.content = ttk.Frame(self)
        self.content.grid(row=0, column=0, sticky='wens')
        
        title = ttk.Label(self.content, text=m['title'])
        title.grid(row=0,column=0, sticky='we')
        
        if 'tkwidget' in m.keys():
            self.mod = m['tkwidget'](master=self.content,
                                     farm=self.farm)
            self.mod.grid(row=1, column=0, sticky='we')

def get_module(modules, iid):
    for m in modules:
        if m['id'] == iid:
            return m
        elif 'submodules' in m.keys():
            r = get_module(modules=m['submodules'], 
                              iid=iid)
            if r is not None:
                return r
            
    return None

def start(path = None):
    # check if config file
    config_file_path = 'paille_gui.config'
    if os.path.isfile(config_file_path):
        f = open(config_file_path, "r")
        file_to_test_path = f.readline() 
        if os.path.isfile(file_to_test_path):
            path = file_to_test_path
    
    window = MainWindow(modules=modules)
    
    if path is not None:
        window.open_farm(path)
    
    window.mainloop()
