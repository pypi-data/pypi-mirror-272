# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import messagebox

from ttkthemes import ThemedTk

import numpy as np
import os
import tksheet

import csv

from ...farm import Farm
from ...table import timestamp_to_date, date_to_timestamp

from ..widget import ComboboxDict, ScrollbarFrame, ValueEntry

class OrderFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.distribution_list_frame = None
        
        self.distribution_list_frame = DistributionListFrame(
                                        master=self, 
                                        farm=self.farm)
        self.distribution_list_frame.grid(row=0, column=0, sticky='wen')
        
        self.order_frame = None
        
        # open first distribution
        self.distribution_list_frame.on_select()
    
    def open_order_frame(self, 
                         sales_distribution_id,
                         sales_order_id=None):
        if self.order_frame is not None:
            self.order_frame.destroy()
        
        self.order_frame = OrderByDistributionFrame(master=self, 
                                                    farm=self.farm, 
                                                    sales_distribution_id=sales_distribution_id,
                                                    sales_order_id=sales_order_id)
        self.order_frame.grid(row=1, column=0, sticky='wn')
        
        
class DistributionListFrame(ttk.Frame):
    
    def __init__(self, 
                 master, 
                 farm:Farm):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master, width=300)
        
        distribution = self.farm.sales.distribution.get_entries(columns=['id',
                                                                          'date'],
                                                                list_dict=True,
                                                                order_by='date DESC')
        first_id = distribution[0]['id']
        distribution = {timestamp_to_date(d['date']) : d['id'] for d in distribution}
        
        self.distribution_CB = ComboboxDict(self, values=distribution, width=12)
        self.distribution_CB.grid(row=0, column=0, pady=5, padx=10, sticky='w')
        self.distribution_CB.bind("<<ComboboxSelected>>", self.on_select)
        self.distribution_CB.set_id(first_id)
        
        # GOODS LIST
        # define columns
        # columns = ('date')
        
        # self.tree = ttk.Treeview(self, 
                                 # columns=columns, 
                                 # show='headings', 
                                 # selectmode="browse",
                                 # height=18)
        
        # define headings
        # self.tree.heading('date', text='Date', anchor=tk.W)
        
        # self.tree.column('date', width=70)
        
        # self.fill()
        
        # self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        # scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        # self.tree.configure(yscroll=scrollbar.set)
        # scrollbar.grid(row=0, column=1, sticky='wns')
        
        ttk.Button(self, text="Actualiser", command=self.on_select)\
            .grid(row=0, column=1, pady=5, padx=10, sticky='e')
        
        ttk.Button(self, text="Importer", command=self.import_data)\
            .grid(row=0, column=2, pady=5, padx=10, sticky='e')
        
        ttk.Button(self, text="Générer", command=self.report)\
            .grid(row=0, column=3, pady=5, padx=10, sticky='e')
        
    
    # def fill(self):
        # distribution = self.farm.sales.order.count_by_sales_distribution()
        
        # distribution = self.farm.sales.distribution.get_entries(columns=['id',
                                                                         # 'date'],
                                                                # list_dict=True,
                                                                # order_by='date DESC')
        
        # for g in distribution:
            # date_str = timestamp_to_date(g['date'])
            # self.tree.insert('', tk.END, g['id'], 
                             # values=[date_str])
    
    # def refresh(self, item_id, focus=True):
        # self.tree.delete(*self.tree.get_children())
        # self.fill()
        
        # if item_id is not None:
            # if focus:
                # self.tree.focus(item_id)
            # self.tree.selection_set(item_id)
    
    def on_select(self, *event):
        sales_distribution_id = self.distribution_CB.get_id()
        print("you clicked on distribution id", sales_distribution_id)
            
        self.master.open_order_frame(sales_distribution_id=sales_distribution_id)
    
    def import_data(self, *event):
        import_window = ImportWindow(parent=self,
                                     farm = self.farm)
    
    def report(self, *event):
        sales_distribution_id = self.distribution_CB.get_id()
            
        # if len(sales_distribution_id) == 0:
        #     messagebox.showinfo("paille", "Sélectionnez une distribution et recommencez.")
        
        #     return False
        
        sales_distribution_id = int(sales_distribution_id)
        
        distribution = self.farm.sales.distribution.get_entry(sales_distribution_id)
        
        path_prefix = timestamp_to_date(distribution['date'], date_format ='%Y-%m-%d')
        path_prefix +='_paille_'+self.farm.file_name+'_commandes'

        self.farm.sales.order.report(sales_distribution_id=sales_distribution_id, 
                                      open_file=True, 
                                      path_prefix=path_prefix,
                                      debug_mode=False,
                                      clean=True)     
    
class OrderByDistributionFrame(ttk.Frame):
    def __init__(self, 
                 master, 
                 farm:Farm, 
                 sales_distribution_id,
                 sales_order_id=None):
        self.sales_distribution_id = sales_distribution_id
        self.farm = farm
        
        ttk.Frame.__init__(self, master)
        
        self.orders, self.deliveries, self.goods = self.farm.sales.product.get_orders_and_producs_by_distribution(sales_distribution_id=self.sales_distribution_id)
        
        self.deliveries_id = {d['name'] : i for i, d in self.deliveries.iterrows()}
        
        headers = self.orders.columns.to_list()
        headers[0] = 'Client'
        headers[1] = 'id'
        headers[2] = 'Livraison'
        
        self.headers = headers.copy()
        
        self.product_col = {}
        self.product_col_inverse = {}
        for g_id, g in self.goods.iterrows():
            self.product_col[g_id] = headers.index(g_id)
            self.product_col_inverse[self.product_col[g_id]] = g_id
            headers[self.product_col[g_id]] = g['code']
        
        data = [headers]
        data += [[i for i in j] for j in self.orders.values]
        
        # on retire les 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == 0.0 or data[i][j] == '0.0':
                    data[i][j] = ''
                # on enlève les virgules en trop
                elif i > 0 and j > 2:
                    if float(int(data[i][j])) == data[i][j]:
                        data[i][j] = int(data[i][j])
        
        self.sheet = tksheet.Sheet(self,
                                   data = data,
                                   height=550,
                                   width=900,
                                   row_drag_and_drop_perform=False,
                                   column_drag_and_drop_perform=False,
                                   expand_sheet_if_paste_too_big=True)
        
        self.sheet.headers(0, redraw=True)
        self.sheet.row_index(0, redraw=True)
        self.sheet.hide_columns(columns=[1])
        self.sheet.hide_rows(rows=0)
        
        self.sheet.set_all_column_widths(width=None)
        
        self.sheet.set_index_width(pixels=150)
        self.sheet.set_header_height_lines(2)
        
        self.sheet.table_align(align='right')
        self.sheet.row_index_align(align='left')
        
        self.sheet.change_theme(theme='light blue')
        
        # products colors:
        self.set_column_colors()
        
        self.refresh_headers_sum()
        
        
        # client
        self.clients = self.farm.sales.client.get_entries(columns=['id',
                                                  'name',
                                                  'first_name'],
                                         order_by="UPPER(name), UPPER(first_name)",
                                         pandas=True)
        
        self.client_id = {c['name']+' '+c['first_name'] : c['id'] for i, c in self.clients.iterrows()}
        
        client_column = 0
        self.sheet.align((None, client_column), align='left')
        for r, o in self.orders.iterrows():
            sales_client_name = o['sales_client_name']
            if sales_client_name is None:
                sales_client_name = '?'
            self.sheet.dropdown(
                (r+1, client_column), # +1 due to the header
                values=['?']+[c['name']+' '+c['first_name'] for i, c in self.clients.iterrows()],
                set_value=sales_client_name
                )
        
        # delivery
        self.sheet.align((None, 2), align='left')
        for r, o in self.orders.iterrows():
            sales_delivery_name = o['sales_delivery_name']
            if sales_delivery_name is None:
                sales_delivery_name = '?'
            self.sheet.dropdown(
                (r+1, 2), # +1 due to the header
                values=['?']+list(self.deliveries['name'].values),
                set_value=sales_delivery_name
                )
            
        self.sheet.enable_bindings(["single_select",
                                    "drag_select",
                                    # "shift_select",
                                    "ctrl_select",
                                    "row_select",
                                    # "toggle_select",
                                    "arrowkeys",
                                    "undo",
                                    "copy",
                                    "cut",
                                    "paste",
                                    "edit_cell",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "delete",
                                    # "rc_insert_row",
                                    # "rc_delete_row",
                                    ])
        
        self.sheet.extra_bindings(bindings=["end_edit_cell",
                                            "end_paste"],
                                   func=self.sheet_edit_cell_event)
        
        self.sheet.extra_bindings(bindings=["delete",
                                            "end_cut"],
                                  func=self.sheet_delete_event)
        
        # self.sheet.extra_bindings(bindings=["rc_delete_row"],
                                  # func=self.sheet_delete_row_event)
        
        self.sheet.extra_bindings(bindings=["undo"],
                                  func=self.sheet_undo_event)
        
        self.sheet.extra_bindings(bindings=["shift_row_select"],
                                  func=self.sheet_shift_row_select_event)
        
        self.sheet.extra_bindings(bindings=["paste"],
                                   func=self.sheet_paste_event)
        
        # self.sheet.extra_bindings(bindings=["rc_insert_row"],
                                  # func=self.sheet_insert_row_event)
        
        self.sheet.set_options(copy_label="Copier")
        self.sheet.set_options(cut_label="Couper")
        self.sheet.set_options(paste_label="Coller")
        self.sheet.set_options(edit_cell_label="Éditer")
        self.sheet.set_options(delete_label="Supprimer")
        # self.sheet.set_options(delete_rows_label="Supprimer cette commande")
        # self.sheet.set_options(insert_rows_above_label="Ajouter une commande au dessus")
        # self.sheet.set_options(insert_rows_below_label="Ajouter une commande en dessous")
        
        self.sheet.popup_menu_add_command(
            "Ajouter une commande",
            self.add_order,
            table_menu=False,
            header_menu=False,
            index_menu=True,
            empty_space_menu=True,
        )
        
        self.sheet.popup_menu_add_command(
            "Supprimer cette commande",
            self.delete_order,
            table_menu=False,
            header_menu=False,
            index_menu=True,
            empty_space_menu=False,
        )
        
        self.sheet.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='nwes')
        
        # values = {c[1] : c[0] for c in self.clients}
        # values[''] = None
        
        # self.client_combobox = ComboboxDict(self, 
                  # width=30, 
                  # values=values)
        # self.client_combobox.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        # ttk.Button(self, text="Ajouter", command=self.add_client)\
            # .grid(row=1, column=1, padx=5, pady=2, sticky='w')
        
        # on ajoute une ligne à la fin
        self.sheet_add_row()
    
    def set_column_colors(self):
        for g_id, g in self.goods.iterrows():
            if len(g['color']) > 0:
                self.sheet.highlight((None, self.product_col[g_id]),
                                     bg=g['color'])
    
    def add_order(self, *event):
        rows = self.sheet.get_selected_rows(
                    get_cells_as_rows= True,
                    return_tuple = True,
                    )
        n = len(self.sheet.get_selected_rows(
                    get_cells_as_rows= True,
                    return_tuple = True,
                    ))
        
        if n == 0:
            n=1
            
        self.sheet_add_row(i=int(np.max(rows))+2, n=n)
        
    
    def refresh_headers_sum(self):
        for i_col in range(3, len(self.orders.columns.to_list())):
            self.refresh_header_sum(i_col)
        
    def refresh_header_sum(self, i_col):
        # get values
        col_values = self.sheet.span((1, i_col), expand="down").data
        
        if type(col_values) is not list:
            col_values = [col_values]
        
        s = 0
        # si vide, c'est que ça vaut 0
        for i in range(len(col_values)):
            if col_values[i] != '':
                s += float(col_values[i])
        
        # s = np.array(col_values).astype(float).sum()
        print('refresh col', i_col, s)
        span = self.sheet.span((0, i_col))
        span.data = self.goods.loc[self.headers[i_col],'code']+'\n'+str(s)
    
    def sheet_edit_cell(self, r, c, q=None):
        sales_order_id = self.sheet[r,1].data
        
        # d'abord on vérifie que la ligne possède un id
        # si ce n'est pas le cas, on lui ajoute
        if sales_order_id == 'na':
            sales_order_id = self.farm.sales.order.insert_entry(sales_distribution_id=self.sales_distribution_id,
                                                                sales_delivery_id=None,
                                                                sales_client_id=None)
            self.sheet.span((r,1)).data = sales_order_id
            
            # ajouter une nouvelle ligne si cette ligne est la dernière
            init_total_rows = self.sheet.get_total_rows(include_index=True)
            if r == init_total_rows - 1:
                self.sheet_add_row(i=None, n=1)
                self.sheet.select_cell(r, c-1)
        
        print('edit', r, c, sales_order_id)
        
        if c in self.product_col_inverse.keys():
            # it is a quantity edit !
            if q is None:
                q = self.sheet[r,c].data
            
            if q == '':
                q = 0
            elif q == 0:
                self.sheet[r,c].data = ''
            else:
                q = float(q)
            
            # check virgules
            if q > 0 and float(int(q)) == q:
                self.sheet[r,c].data = int(q)
            
            logistic_goods_id = self.product_col_inverse[c]
            sales_product = self.farm.sales.product.get_entries(columns=['id'],
                                                where='sales_order_id='+str(sales_order_id)+' AND logistic_goods_id='+str(logistic_goods_id))
            
            if len(sales_product)>0:
                sales_product_id = sales_product[0][0]
                if q == 0:
                    self.farm.sales.product.delete_entry(i=sales_product_id)
                else:
                    self.farm.sales.product.update_entry(i=sales_product_id, 
                                                         quantity=q)
            elif q > 0:
                self.farm.sales.product.insert_entry(sales_order_id=sales_order_id,
                                                     logistic_goods_id=logistic_goods_id,
                                                     quantity=q)
            
            # edit headers
            self.refresh_header_sum(i_col=c)
            
        elif c == 0:
            # it is a client edit !
            sales_client_full_name = str(self.sheet.span((r,c)).data)
            
            if sales_client_full_name != "?":
                sales_client_id = self.client_id[sales_client_full_name]
            else:
                sales_client_id = None
                
            # print('!', sales_client_full_name, sales_client_id)
            
            self.farm.sales.order.update_entry(i=sales_order_id, 
                                                sales_client_id=sales_client_id)
        
        elif c == 2:
            # it is a delivery edit !
            sales_delivery_name = str(self.sheet.span((r,c)).data)
            if sales_delivery_name != "?":
                sales_delivery_id = self.deliveries_id[sales_delivery_name]
            else:
                sales_delivery_id = None
                
            self.farm.sales.order.update_entry(i=sales_order_id, 
                                               sales_delivery_id=sales_delivery_id)
       
        
            
    def sheet_add_row(self, i=None, n=1):
        init_total_rows = self.sheet.get_total_rows(include_index=True)
        init_total_columns = self.sheet.get_total_columns()
        
        if i is None:
            i = init_total_rows
        
        self.sheet.insert_rows(
                rows=n,
                idx=i,
                row_index=True,
                fill=False,
                undo=False,
                emit_event=False,
                redraw=True,
            )
        
        
        for i in range(i, i + n):
            self.sheet_add_dropdown(i=i)
            
            for c in range(3, init_total_columns):
                self.sheet.span((i,c)).data = ''
            
            # sales_order_id = self.farm.sales.order.insert_entry(sales_distribution_id=self.sales_distribution_id,
                                                                # sales_delivery_id=None,
                                                                # sales_client_id=None)
            # on met 'na' à l'id. 
            # si on édite la ligne, un id sera attribué
            self.sheet.span((i,1)).data = 'na'
            
        self.set_column_colors()
    
    def sheet_add_dropdown(self, i, 
                           set_delivery_value='?',
                           set_client_value='?'):
        # delivery
        self.sheet.align((i, 2), align='left')
        self.sheet.dropdown(
            (i, 2),
            values=['?']+list(self.deliveries['name'].values),
            set_value= set_delivery_value
            )
        
        # client
        self.sheet.align((i, 0), align='left')
        self.sheet.dropdown(
            (i, 0),
            values=['?']+[c['name']+' '+c['first_name'] for i, c in self.clients.iterrows()],
            set_value=set_client_value
            )
    
    def sheet_edit_cell_event(self, event):
        couples = list(event.cells.table.keys())
        
        for r,c in couples:
            self.sheet_edit_cell(r, c)
    
    def sheet_undo_event(self, event):
        print(event)
        couples = list(event.cells.table.keys())
        
        for r,c in couples:
            print('undo', r,c)
            self.sheet_edit_cell(r, c)
    
    def sheet_delete_event(self, event):
        couples = list(event.cells.table.keys())
        # print(couples)
        for r, c in couples:
            if c == 2 or c == 0:
                self.sheet.span((r,c)).data = "?"
                self.sheet_edit_cell(r, c)
            else:
                self.sheet.span((r,c)).data = ''
                self.sheet_edit_cell(r, c, q=0)
    
    def sheet_shift_row_select_event(self, event):
        # event.
        print(event)
    
    def delete_order(self, *event):
        rows = self.sheet.get_selected_rows(
                    get_cells_as_rows= True,
                    return_tuple = True,
                    )
        rows = [r+1 for r in rows] # because header
        
        if askyesno(title="Suppression",
                    message="Etes-vous sûrs de vouloir supprimer cette commande ?\nCette action sera irréversible."):
        
            sales_order_id_list = []
            for r in rows:
                sales_order_id = self.sheet.span((r, 1)).data
                sales_order_id_list.append(sales_order_id)
                self.farm.sales.order.delete_entry(i=sales_order_id)
            
            # for sales_order_id in sales_order_id_list:
            #     # on récupère la ligne
            #     id_col_values = self.sheet.span((1, 1), expand="down").data
            #     self.sheet.del_row(idx=id_col_values.index(sales_order_id)+2, # because header...
            #                        emit_event=False,
            #                        undo=False,
            #                        redraw=True)
            
            # il y a un bug quand on veut supprimer la dernière ligne
            # donc méthode plus radicale : on rafraîchi le tableur.
            self.master.distribution_list_frame.on_select()
        
        
            
    def sheet_paste_event(self, *event):
        # le tableur est agrandi si besoin.
        # mais il faut ajouter des id aux nouvelles lignes
        # et refaire les couleurs des colonnes
        # et refaire les sommes.
        
        # d'abord les id
        total_rows = self.sheet.get_total_rows(include_index=True)
        total_columns = self.sheet.get_total_columns()
        
        for r in range(total_rows):
            if self.sheet.span((r, 1)).data in ['na', '']:
                # on lui attribue un id
                sales_order_id = self.farm.sales.order.insert_entry(sales_distribution_id=self.sales_distribution_id,
                                                                    sales_delivery_id=None,
                                                                    sales_client_id=None)
                self.sheet.span((r,1)).data = sales_order_id
                
                # on sauvegarde les éléments
                for c in range(total_columns):
                    self.sheet_edit_cell(r=r, c=c)
                
                # on ajoute une ligne éventuellement
                if r == total_rows - 1:
                    self.sheet_add_row(i=None, n=1)
                    # self.sheet.select_cell(r, c-1)
                
                # on ajoute les dropdown
                self.sheet_add_dropdown(i=r,
                                        set_delivery_value=self.sheet.span((r,2)).data,
                                        set_client_value=self.sheet.span((r,0)).data)
                
        
        # on applique les couleurs
        self.set_column_colors()
        
        # on calcule les sommes d'entêtes
        self.refresh_headers_sum()
        

class ImportWindow(ThemedTk):

    def __init__(self, parent, farm):
        self.parent = parent
        self.farm = farm
        
        # tk.Tk.__init__(self)
        ThemedTk.__init__(self, theme="arc") 
        self.title('Importer des données')
        self.geometry("200x200")
        
        self.file_name = ''
        
        data_type_list = ['EBE', 'Cagette', 'CAMAP']
        
        ttk.Label(self, text='Type')\
            .grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.data_type = ttk.Combobox(self, 
                     values=data_type_list,
                     width=10)
        self.data_type.grid(row=0, column=1, pady=10, padx=5, sticky='w')
        
        ttk.Button(self, text="Choisir le fichier", command=self.choose_file)\
            .grid(row=1, column=0, columnspan=2, pady=5, padx=10, sticky='we')
        
        self.file_name_label = ttk.Label(self, text=self.file_name)
        self.file_name_label.grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky='w')
    
        ttk.Button(self, text="Importer", command=self.import_data)\
            .grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky='we')
    
    def choose_file(self, *event):
        self.file_name = tk.filedialog.askopenfilename(title='Choisir un fichier', filetypes=[("Fichier CSV", ".csv")], parent=self)
        self.file_name_label.config(text=os.path.splitext(os.path.basename(self.file_name))[0]+'.csv')
        
    def import_data(self, *event):
        
        print(self.data_type.get(), self.file_name)
        
        with open(self.file_name) as f:
            reader = csv.reader(f)
            data = list(reader)
        
        print(data)
        
        # on ajoute les commandes avec self.farm direct dans la DB
        
        # on actualise la tksheet
        self.parent.on_select()
        
        self.destroy()  
        
        