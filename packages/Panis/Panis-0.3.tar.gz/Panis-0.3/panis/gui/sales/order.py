# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import messagebox


from ...farm import Farm
from ...table import timestamp_to_date, date_to_timestamp


from ..widget import ComboboxDict, ScrollbarFrame, ValueEntry

class OrderFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.distribution_list_frame = None
        self.delivery_list_frame = None
        self.order_list_frame = None
        self.product_frame = None
        
        self.refresh()
        
    def refresh(self, 
                sales_distribution_id=None,
                sales_delivery_id=None,
                sales_order_id=None,
                destroy=True):
        
        if destroy:
            self.distribution_list_frame = DistributionListFrame(
                                        master=self, 
                                        farm=self.farm,
                                        sales_distribution_id=sales_distribution_id,
                                        sales_delivery_id=sales_delivery_id, 
                                        sales_order_id=sales_order_id)
            self.distribution_list_frame.grid(row=0, column=0, sticky='wn')
        else:
            if sales_distribution_id is not None\
                and self.distribution_list_frame is not None:
                self.distribution_list_frame.refresh(sales_distribution_id,
                                                     focus=False)
            
            if sales_delivery_id is not None\
                and self.delivery_list_frame is not None:
                self.delivery_list_frame.refresh(sales_delivery_id,
                                                 focus=False)
                
            if sales_order_id is not None\
                and self.order_list_frame is not None:
                self.order_list_frame.refresh(sales_order_id,
                                              focus=False)
        
class DistributionListFrame(ttk.Frame):
    
    def __init__(self, 
                 master, 
                 farm:Farm,
                 sales_distribution_id=None,
                 sales_delivery_id=None,
                 sales_order_id=None):
        
        self.farm = farm
        self.master = master
        
        self.sales_distribution_id = sales_distribution_id
        self.sales_delivery_id  =sales_delivery_id
        self.sales_order_id = sales_order_id
        # self.delivery_list_frame = None
        
        ttk.Frame.__init__(self, master)
        # GOODS LIST
        # define columns
        columns = ('date', 'count_order', 'product_sum')
        
        self.tree = ttk.Treeview(self, 
                                 columns=columns, 
                                 show='headings', 
                                 selectmode="browse",
                                 height=18)
        
        # define headings
        self.tree.heading('date', text='Date', anchor=tk.W)
        self.tree.heading('count_order', text='n', anchor=tk.E)
        self.tree.heading('product_sum', text='p', anchor=tk.E)
        
        self.tree.column('date', width=70)
        self.tree.column('count_order', width=30, anchor=tk.E)
        self.tree.column('product_sum', width=40, anchor=tk.E)
        
        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
        
        if sales_distribution_id is not None:
            self.select(sales_distribution_id)
        
        ttk.Button(self, text="Générer les feuilles\n de livraison", command=self.report)\
            .grid(row=1, column=0, columnspan=2, pady=10, padx=5)
        
        copy_LF = ttk.LabelFrame(self, text="Copier la livraison")
        copy_LF.grid(row=2, column=0, columnspan=2, pady=10, padx=5)
        
        ttk.Label(copy_LF, text="date")\
            .grid(row=0, column=0, sticky="w", padx=5, pady=2, columnspan=2)
        
        self.copy_date_variable = tk.StringVar()
        
        ttk.Entry(copy_LF, 
                  textvariable=self.copy_date_variable,
                  width=10)\
            .grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Button(copy_LF, text="Copier", command=self.copy)\
            .grid(row=1, column=1, sticky="w", padx=5, pady=2)
    
    
    def clean(self):
        self.sales_distribution_id = None
        self.sales_delivery_id  =None
        self.sales_order_id = None
    
    def fill(self):
        distribution = self.farm.sales.order.count_by_sales_distribution()
        
        for g in distribution:
            date_str = timestamp_to_date(g['date'])
            self.tree.insert('', tk.END, g['id'], 
                             values=[date_str,
                                     g['count_order'],
                                     g['product_sum']])
    
    def refresh(self, item_id, focus=True):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            if focus:
                self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def select(self, item_id, destroy=True):
        self.tree.focus(item_id)
        if destroy:
            self.tree.selection_set(item_id)
    
    def on_select(self, event):
        sales_distribution_id = self.tree.focus()
        if len(sales_distribution_id) > 0:
            print("you clicked on distribution id", sales_distribution_id)
            
            if self.master.delivery_list_frame is not None:
                if self.master.order_list_frame is not None:
                    if self.master.product_frame is not None:
                        self.master.product_frame.destroy()
                    self.master.order_list_frame.destroy()
                self.master.delivery_list_frame.destroy()
            
            self.master.delivery_list_frame = DeliveryListFrame(master=self.master, 
                                                         farm=self.farm, 
                                                         sales_distribution_id=sales_distribution_id,
                                                         sales_delivery_id=self.sales_delivery_id,
                                                         sales_order_id=self.sales_order_id)
            self.master.delivery_list_frame.grid(row=0, column=1, sticky='wns', padx=5)
            
            self.clean()
    
    def report(self, *event):
        sales_distribution_id = self.tree.focus()
            
        if len(sales_distribution_id) == 0:
            messagebox.showinfo("paille", "Sélectionnez une distribution et recommencez.")
        
            return False
        
        sales_distribution_id = int(sales_distribution_id)
        
        distribution = self.farm.sales.distribution.get_entry(sales_distribution_id)
        
        path_prefix = timestamp_to_date(distribution['date'], date_format ='%Y-%m-%d')
        path_prefix +='_paille_'+self.farm.file_name+'_commandes'

        self.farm.sales.order.report(sales_distribution_id=sales_distribution_id, 
                                      open_file=True, 
                                      path_prefix=path_prefix,
                                      debug_mode=False,
                                      clean=True)     
    
    def copy(self):
        input_sales_distribution_id = self.tree.focus()
            
        if len(input_sales_distribution_id) == 0:
            messagebox.showinfo("paille", "Sélectionnez une distribution et recommencez.")
        
            return False
        
        input_sales_distribution_id = int(input_sales_distribution_id)
    
        output_distribution = self.farm.sales.distribution.get_entries(columns=['id'],
                                                                where="date="+str(date_to_timestamp(self.copy_date_variable.get())),
                                                                list_dict=True)
        if len(output_distribution) > 0:
            output_sales_distribution_id = output_distribution[0]['id']
            
            copy_distribution(farm=self.farm, 
                              output_sales_distribution_id=output_sales_distribution_id, 
                              input_sales_distribution_id=input_sales_distribution_id)
            
        self.master.refresh(sales_distribution_id=input_sales_distribution_id,
                            destroy=False)
    
class DeliveryListFrame(ttk.Frame):
    def __init__(self, 
                 master, 
                 farm:Farm, 
                 sales_distribution_id, 
                 sales_delivery_id=None,
                 sales_order_id=None,
                 **args):
        self.farm = farm
        self.sales_distribution_id = sales_distribution_id
        self.sales_delivery_id = sales_delivery_id
        self.sales_order_id = sales_order_id
        
        ttk.Frame.__init__(self, master)
        # GOODS LIST
        # define columns
        columns = ('name', 'count_order', 'product_sum')
        
        self.tree = ttk.Treeview(self,
                                 columns=columns,
                                 show='headings',
                                 selectmode="browse",
                                 height=22)
        
        # define headings
        self.tree.heading('name', text='Livraison', anchor=tk.W)
        self.tree.heading('count_order', text='n', anchor=tk.E)
        self.tree.heading('product_sum', text='p', anchor=tk.E)

        self.tree.column('name', width=120)
        self.tree.column('count_order', width=30, anchor=tk.E)
        self.tree.column('product_sum', width=40, anchor=tk.E)
        
        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
        
        if sales_delivery_id is not None:
            self.select(sales_delivery_id)
        
        copy_LF = ttk.LabelFrame(self, text="Copier la livraison")
        copy_LF.grid(row=1, column=0, columnspan=2, pady=10, padx=5)
        
        ttk.Label(copy_LF, text="date")\
            .grid(row=0, column=0, sticky="w", padx=5, pady=2, columnspan=2)
        
        self.copy_date_variable = tk.StringVar()
        
        ttk.Entry(copy_LF, 
                  textvariable=self.copy_date_variable,
                  width=10)\
            .grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Button(copy_LF, text="Copier", command=self.copy)\
            .grid(row=1, column=1, sticky="w", padx=5, pady=2)
    
        
    def clean(self):
        self.sales_delivery_id = None
        self.sales_order_id = None
    
    def fill(self):
        delivery = self.farm.sales.order.count_by_sales_delivery(sales_distribution_id=self.sales_distribution_id)
        
        for g in delivery:
            self.tree.insert('', tk.END, g['id'], 
                             values=[g['name'],
                                     g['count_order'],
                                     g['product_sum']])
    
    def refresh(self, item_id, focus=True):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            if focus:
                self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def select(self, item_id):
        self.tree.focus(item_id)
        self.tree.selection_set(item_id)
    
    def on_select(self, event):
        sales_delivery_id = self.tree.focus()
        
        if len(sales_delivery_id) > 0:
            print("you clicked on delivery id", sales_delivery_id)
            
            if self.master.order_list_frame is not None:
                if self.master.product_frame is not None:
                    self.master.product_frame.destroy()
                self.master.order_list_frame.destroy()
            
            
            self.master.order_list_frame = OrderListFrame(master=self.master, 
                                                   farm=self.farm, 
                                                   sales_distribution_id=self.sales_distribution_id, 
                                                   sales_delivery_id=sales_delivery_id,
                                                   sales_order_id = self.sales_order_id)
            self.master.order_list_frame.grid(row=0, column=2, sticky='wns', padx=5)
            
            self.clean()
        
    def copy(self):
        input_sales_delivery_id = self.tree.focus()
            
        if len(input_sales_delivery_id) == 0:
            messagebox.showinfo("paille", "Sélectionnez une livraison et recommencez.")
        
            return False
        
        input_sales_delivery_id = int(input_sales_delivery_id)
    
        output_distribution = self.farm.sales.distribution.get_entries(columns=['id'],
                                                                where="date="+str(date_to_timestamp(self.copy_date_variable.get())),
                                                                list_dict=True)
        if len(output_distribution) > 0:
            output_sales_distribution_id = output_distribution[0]['id']
            
            copy_delivery(farm=self.farm, 
                          output_sales_distribution_id=output_sales_distribution_id,
                          input_sales_distribution_id=self.sales_distribution_id, 
                          input_sales_delivery_id=input_sales_delivery_id)
            
        self.master.refresh(sales_distribution_id=self.sales_distribution_id,
                            sales_delivery_id=input_sales_delivery_id,
                            destroy=False)
            
class OrderListFrame(ttk.Frame):
    def __init__(self, 
                 master, 
                 farm:Farm, 
                 sales_distribution_id, 
                 sales_delivery_id,
                 sales_order_id=None,
                 **args):
        self.farm = farm
        self.sales_distribution_id = sales_distribution_id
        self.sales_delivery_id = sales_delivery_id
        self.sales_order_id = sales_order_id
        
        self.product_frame = None
        
        ttk.Frame.__init__(self, master)
        
        self.colf = CreateOrderLabelFrame(self, 
                                          farm=self.farm,
                                          sales_distribution_id=self.sales_distribution_id,
                                          sales_delivery_id=self.sales_delivery_id)
        self.colf.grid(row=0, column=0, columnspan=2)
        
        # define columns
        columns = ('name', 'count_product')
        
        self.tree = ttk.Treeview(self, 
                                 columns=columns,
                                 show='headings', 
                                 selectmode="browse",
                                 height=19)
        
        # define headings
        self.tree.heading('name', text='Commande', anchor=tk.W)
        self.tree.heading('count_product', text='p', anchor=tk.E)

        self.tree.column('name', width=130)
        self.tree.column('count_product', width=40, anchor=tk.E)

        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=1, column=0, sticky='wns', pady=5)
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ens')
        
        
        if sales_order_id is not None:
            self.select(sales_order_id)
        
        copy_LF = ttk.LabelFrame(self, text="Copier la commande")
        copy_LF.grid(row=2, column=0, columnspan=2, pady=10, padx=5)
        
        ttk.Label(copy_LF, text="date")\
            .grid(row=0, column=0, sticky="w", padx=5, pady=2, columnspan=2)
        
        self.copy_date_variable = tk.StringVar()
        
        ttk.Entry(copy_LF, 
                  textvariable=self.copy_date_variable,
                  width=10)\
            .grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Button(copy_LF, text="Copier", command=self.copy)\
            .grid(row=1, column=1, sticky="w", padx=5, pady=2)
    
    def copy(self):
        input_sales_order_id = self.tree.focus()
            
        if len(input_sales_order_id) == 0:
            messagebox.showinfo("paille", "Sélectionnez une commande et recommencez.")
            
            return False
            
        input_sales_order_id = int(input_sales_order_id)
    
        output_distribution = self.farm.sales.distribution.get_entries(columns=['id'],
                                                                where="date="+str(date_to_timestamp(self.copy_date_variable.get())),
                                                                list_dict=True)
        if len(output_distribution) > 0:
            output_sales_distribution_id = output_distribution[0]['id']
            
            copy_order(farm=self.farm,
                       output_sales_distribution_id=output_sales_distribution_id,
                       input_sales_order_id=input_sales_order_id)
            
        self.master.refresh(sales_distribution_id=self.sales_distribution_id,
                            sales_delivery_id=self.sales_delivery_id,
                            sales_order_id=None,
                            destroy=False)
        
    def clean(self):
        self.sales_order_id = None
    
    def fill(self):
        client = self.farm.sales.order.get_clients(sales_distribution_id=self.sales_distribution_id,
                                                   sales_delivery_id=self.sales_delivery_id)
        
        for g in client:
            self.tree.insert('', tk.END, g['sales_order_id'], 
                             values=[g['name'],
                                     g['p']])
    
    def refresh(self, item_id, focus=True):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            if focus:
                self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def select(self, item_id):
        self.tree.focus(item_id)
        self.tree.selection_set(item_id)
    
    def on_select(self, event):
        sales_order_id = self.tree.focus()
        if len(sales_order_id) > 0:
            print("you clicked on order id", sales_order_id)
            
            if self.master.product_frame is not None:
                self.master.product_frame.destroy()
            
            self.master.product_frame = ProductFrame(master=self.master,
                                              farm=self.farm,
                                              sales_distribution_id=self.sales_distribution_id, 
                                              sales_delivery_id=self.sales_delivery_id,
                                              sales_order_id=sales_order_id)
            self.master.product_frame.grid(row=0, column=3, sticky='wns', padx=5)
            
            self.clean()
    
    def remove(self, *event):
        sales_order_id = self.tree.focus()
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer cette commande ?"):
            self.farm.sales.order.delete_entry(i=sales_order_id)
            
            self.master.refresh(sales_distribution_id=self.sales_distribution_id,
                                sales_delivery_id=self.sales_delivery_id,
                                sales_order_id=None)
    
        
class CreateOrderLabelFrame(ttk.LabelFrame):
    def __init__(self, 
                 master, 
                 farm, 
                 sales_distribution_id, 
                 sales_delivery_id):
        self.master = master
        self.farm = farm
        self.sales_distribution_id = sales_distribution_id
        self.sales_delivery_id = sales_delivery_id
        
        ttk.LabelFrame.__init__(self, master, text="Nouveau")
        
        self.create_client_combobox()
                
        button1 = ttk.Button(self, text = "Ajouter", command=self.new)
        button1.grid(sticky="W",row=0,column=1, padx=5, pady=5)
    
    def create_client_combobox(self):
        clients = self.farm.sales.order.get_remaining_clients(sales_distribution_id=self.sales_distribution_id, 
                                                              sales_delivery_id=self.sales_delivery_id)
        values = {c['name'] : c['id'] for c in clients}
        values[''] = None
        
        self.client_combobox = ComboboxDict(self, 
                  width=10, 
                  state="readonly",
                  values=values)
        self.client_combobox.grid(row=0, column=0, padx=5, pady=5)
    
    def refresh(self):
        self.client_combobox.destroy()
        self.create_client_combobox()
    
    def new(self):
        if self.client_combobox.get_id() is not None:
            iid = self.farm.sales.order.insert_entry(sales_distribution_id=self.sales_distribution_id,
                                                     sales_delivery_id=self.sales_delivery_id,
                                                     sales_client_id=self.client_combobox.get_id())
            
            self.master.master.refresh(sales_distribution_id=self.sales_distribution_id,
                                       sales_delivery_id=self.sales_delivery_id,
                                       sales_order_id=iid)

class ProductFrame(ttk.Frame):
    def __init__(self, 
                 master, 
                 farm:Farm, 
                 sales_distribution_id, 
                 sales_delivery_id,
                 sales_order_id):
        
        self.farm = farm
        self.sales_distribution_id = sales_distribution_id
        self.sales_delivery_id = sales_delivery_id
        self.sales_order_id = sales_order_id
        
        ttk.Frame.__init__(self, master)
        
        # ttk.Button(self, text="Enregistrer la commande", command=self.save)\
            # .grid(row=0, column=0, padx=5, pady=2, sticky="we")
        
        self.create_product_list()
        
    
    def create_product_list(self):
        self.sbf = ScrollbarFrame(self,
                                  width=150, 
                                  height=500,
                                  text="Produits")
        self.sbf.grid(row=0, column=0, sticky='nwes')
        
        products = self.farm.sales.product.get_all_products(i=self.sales_order_id)
        
        self.quantity_value = {}
        
        for i, p in enumerate(products):
            # manque sbf.innercontent..;
            ttk.Label(self.sbf.scrolled_frame, 
                      text=p['code'])\
                .grid(row=i, column=0, padx=2, pady=2, sticky='w')
            
            self.quantity_value[(p['logistic_goods_id'], p['sales_product_id'])] = tk.DoubleVar(value=p['quantity'])
            
            ve = ValueEntry(self.sbf.scrolled_frame, 
                        default=0,
                        width=5,
                        textvariable=self.quantity_value[(p['logistic_goods_id'], p['sales_product_id'])])
            ve.grid(row=i, column=1, pady=2, padx=2)
            # ve.bind('<Return>', self.sbf.self_focus)
            ve.bind('<Return>', 
                    self.save)
            ve.bind('<FocusOut>', 
                    self.save)
            
            ttk.Label(self.sbf.scrolled_frame,
                      text=p['unit'])\
                .grid(row=i, column=2, padx=2, pady=2, sticky='w')
            
        ttk.Button(self, text="Supprimer\n cette commande", command=self.remove)\
            .grid(row=1, column=0, columnspan=1, pady=10, padx=5)
    
            
    def refresh(self):
        self.sbf.destroy()
        self.create_product_list()
    
    def save(self, *event):
        # for all entries, keep only > 0 ones:
        for (logistic_goods_id, _), qv in self.quantity_value.items():
            
            quantity = qv.get()
            if quantity == '':
                quantity = 0
            
            if qv.get() >= 0:
                # check if this product exists
                sp = self.farm.sales.product.get_entries(columns=['id'], 
                                                    where='logistic_goods_id='+str(logistic_goods_id)+' and sales_order_id='+str(self.sales_order_id),
                                                    list_dict=True)
                # if it exists, update
                if len(sp) > 0:
                    if quantity > 0:
                        self.farm.sales.product.update_entry(i=sp[0]['id'], 
                                                             quantity=quantity)
                    if quantity == 0:
                        self.farm.sales.product.delete_entry(i=sp[0]['id'])
                
                elif quantity > 0:
                    # else, create one
                    self.farm.sales.product.insert_entry(sales_order_id=self.sales_order_id,
                                                         logistic_goods_id=logistic_goods_id,
                                                         quantity=quantity)
        
        self.master.refresh(sales_distribution_id=self.sales_distribution_id,
                            sales_delivery_id=self.sales_delivery_id,
                            sales_order_id=self.sales_order_id,
                            destroy=False)
        
    def remove(self, *event):
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer cette commande ?"):
            self.farm.sales.order.delete_entry(i=self.sales_order_id)
            
            self.master.refresh(sales_distribution_id=self.sales_distribution_id,
                                sales_delivery_id=self.sales_delivery_id,
                                sales_order_id=None)

def copy_distribution(farm,
                      output_sales_distribution_id,
                      input_sales_distribution_id):
    input_sales_orders = farm.sales.order.get_entries(columns=['id'],
                                                      where='sales_distribution_id='+str(input_sales_distribution_id),
                                                      list_dict=True)
    for so in input_sales_orders:
        copy_order(farm=farm,
                   output_sales_distribution_id=output_sales_distribution_id,
                   input_sales_order_id=so['id'])

def copy_delivery(farm,
                  output_sales_distribution_id,
                  input_sales_distribution_id,
                  input_sales_delivery_id):
    input_sales_orders = farm.sales.order.get_entries(columns=['id'],
                                                      where='sales_distribution_id='+str(input_sales_distribution_id)+' AND sales_delivery_id='+str(input_sales_delivery_id),
                                                      list_dict=True)
    for so in input_sales_orders:
        copy_order(farm=farm,
                   output_sales_distribution_id=output_sales_distribution_id,
                   input_sales_order_id=so['id'])

def copy_order(farm, 
               output_sales_distribution_id,
               input_sales_order_id):

    input_sales_order = farm.sales.order.get_entry(i=input_sales_order_id)
    
    output_order = farm.sales.order.get_entries(columns=['id'],
                                                     where='sales_distribution_id='+str(output_sales_distribution_id)+' AND sales_delivery_id='+str(input_sales_order['sales_delivery_id'])+' AND sales_client_id='+str(input_sales_order['sales_client_id']),
                                                     list_dict=True)
    if len(output_order) > 0:
        output_order_id = output_order[0]['id']
    else:
        output_order_id = farm.sales.order.insert_entry(sales_distribution_id = output_sales_distribution_id,
                                                             sales_delivery_id = input_sales_order['sales_delivery_id'],
                                                             sales_client_id = input_sales_order['sales_client_id'])
    
    input_products = farm.sales.product.get_entries(columns=['sales_order_id',
                                                            'logistic_goods_id',
                                                            'quantity'],
                                                         where='sales_order_id='+str(input_sales_order_id),
                                                         list_dict=True)
    
    for p in input_products:
        output_product = farm.sales.product.get_entries(columns=['id'],
                                                             where='sales_order_id='+str(output_order_id)+' AND logistic_goods_id='+str(p['logistic_goods_id']),
                                                             list_dict=True)
        if len(output_product) > 0:
            farm.sales.product.update_entry(i=output_product[0]['id'],
                                                 quantity=p['quantity'])
        else:
            farm.sales.product.insert_entry(sales_order_id=output_order_id,
                                                 logistic_goods_id=p['logistic_goods_id'],
                                                 quantity=p['quantity'])

