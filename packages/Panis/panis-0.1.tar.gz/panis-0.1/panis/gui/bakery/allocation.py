# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
# from tkinter.messagebox import askyesno
# from tkinter.filedialog import asksaveasfile

from ...farm import Farm

# import os, sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from ..widget import ScrollbarFrame, ValueEntry
from ...table import timestamp_to_date

class AllocationFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.left_frame = LeftFrame(master=self, 
                                    farm=self.farm)
        self.left_frame.grid(row=0, column=0, sticky='ewn')
        
        self.right_frame = None
        
    def refresh_right_frame(self, sales_distribution_id=None):
        if self.right_frame is not None:
            self.right_frame.destroy()
            self.left_frame.generator_button.grid_forget()
            
        if sales_distribution_id is not None:
            self.right_frame = RightFrame(master=self,
                                          farm=self.farm, 
                                          sales_distribution_id=sales_distribution_id)
            self.right_frame.grid(row=0, column=1, sticky='wn')
            
            self.left_frame.generator_button.grid(row=1, column=0, pady=5, padx=5)
            self.left_frame.generator_button.config(command=self.right_frame.generate)
        
class LeftFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, **args):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master, **args)
        
        self.distribution_list_frame = DistributionListFrame(master=self, 
                                                     farm=self.farm)
        self.distribution_list_frame.grid(row=0, column=0, pady=5, sticky='w')
        
        self.generator_button = ttk.Button(self, 
                   text="Générer les feuilles\nde panification",
                   width=20)
        
class DistributionListFrame(ttk.Frame):
    
    def __init__(self, master, farm:Farm):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master)
        # GOODS LIST
        # define columns
        columns = ('date',)
        
        self.tree = ttk.Treeview(self, 
                                 columns=columns, 
                                 show='headings', 
                                 selectmode="browse",
                                 height=10)
        
        # define headings
        self.tree.heading('date', text='date', anchor=tk.W)
        self.tree.column('date', width=100)
        # self.tree.column('date')
        
        self.fill()
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=0, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ens')
    
    def fill(self):
        distribution = self.farm.sales.distribution.get_entries(columns=['id','date'], 
                                                     order_by='date DESC')
        
        for g in distribution:
            date_str = timestamp_to_date(g[1])
            self.tree.insert('', tk.END, g[0], values=[date_str])
    
    def refresh(self, item_id=None):
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            self.tree.focus(item_id)
            self.tree.selection_set(item_id)
    
    def on_select(self, event):
        sales_distribution_id = self.tree.focus()
        if len(sales_distribution_id) > 0:
            print("you clicked on distribution id", sales_distribution_id)
            
            self.master.master.refresh_right_frame(sales_distribution_id=sales_distribution_id)

class RightFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, sales_distribution_id, **args):
        ttk.Frame.__init__(self, master, **args)
        
        self.sales_distribution_id = sales_distribution_id
        self.farm = farm
        
        self.batches = self.farm.bakery.batch.get_used_batch()
        
        # batches = self.farm.bakery.batch.get_entries(list_dict=True,
        #                                              order_by='position DESC')
        
        # count_batches = self.farm.bakery.process.count_batch()
        # self.batches = []
        # for b in batches:
        #     if b['id'] in count_batches.keys():
        #         self.batches.append(b)
        
        processes = {b['id'] : self.farm.bakery.process.get_dough_id_dict_product_id(bakery_batch_id=b['id']) for b in self.batches}
        
        head = ttk.Frame(self, width=400, height=20)
        head.grid(row=0, column=0, sticky="w")
        
        ttk.Label(head, text="produit", width=8)\
            .grid(row=0, column=0, padx=2, sticky="w")
            
        ttk.Label(head, text='com', width=3, anchor="e")\
            .grid(row=0, column = 1, padx=2, sticky="w")  
        
        ttk.Label(head, text='+', width=2, anchor='center')\
            .grid(row=0, column = 2, padx=2, sticky="w")
        
        ttk.Label(head, text='diff', width=3, anchor="e")\
            .grid(row=0, column = 3, padx=2, sticky="w")    
        
        ttk.Label(head, text='=', width=4, anchor='center')\
            .grid(row=0, column = 4, padx=2, sticky="w")
        
        j_col = 5
        for i, b in enumerate(self.batches):
            ttk.Label(head, text=b['code'], width=5, anchor="center")\
                .grid(row=0, column=j_col, padx=2, sticky="w")
            
            j_col += 1
            if b is not self.batches[-1]:
                ttk.Label(head, text='+', width=2, anchor="center")\
                    .grid(row=0, column=j_col, padx=2, sticky="w")
                j_col += 1
        
        # ttk.Button(head, text="Enregistrer", command=self.save)\
            # .grid(row=0, column=j_col, padx=10, sticky="w")
        
        sbf = ScrollbarFrame(self, width=420, height=500)
        sbf.grid(row=1, column=0, sticky="w")
        
        self.products = self.farm.bakery.allocation.get_products(sales_distribution_id=sales_distribution_id)
        self.products_dict = {p['bakery_product_id'] : p for p in self.products}
        
        self.var_alloc = {}
        
        self.labels = {}
        
        # shape infos
        shape_LF = ttk.Labelframe(self, text='Formats')
        shape_LF.grid(row=1, column=1, sticky='nw')
        self.shapes = self.farm.bakery.shape.get_entries(columns=['id', 'code'],
                                                          list_dict=True,
                                                          order_by='position DESC')
        
        self.shapes_product_list = {s['id'] : [] for s in self.shapes}
        self.shapes_labels = {}
        
        for j, b in enumerate(self.batches):
            ttk.Label(shape_LF, text=b['code'], width=4, anchor='e')\
                .grid(row=0, column=1+j, padx=2, sticky='w')
        
        ttk.Separator(shape_LF, orient='vertical')\
            .grid(row=0, column=1+len(self.batches), rowspan=1+len(self.shapes), padx=2, sticky='ns')
        
        ttk.Label(shape_LF, text='tot.', width=4, anchor='e')\
            .grid(row=0, column=1+len(self.batches)+1, padx=2, sticky='w')
    
        for i, s in enumerate(self.shapes):
            ttk.Label(shape_LF, text=s['code'], anchor='w')\
                .grid(row=1+i, column=0, padx=2, pady=2, sticky='w')
                
            for j, b in enumerate(self.batches):
                self.shapes_labels[(b['id'], s['id'])] = ttk.Label(shape_LF, text='0', anchor='e', width=4)
                self.shapes_labels[(b['id'], s['id'])].grid(row=1+i, column=1+j, padx=2, pady=2, sticky='w')
            
            self.shapes_labels[('tot', s['id'])] = ttk.Label(shape_LF, text='0', anchor='e', width=4)
            self.shapes_labels[('tot', s['id'])].grid(row=1+i, column=2+len(self.batches), padx=2, pady=2, sticky='w')
        
        for i, p in enumerate(self.products):
            
            label_code = ttk.Label(sbf.scrolled_frame, text=p['code'])
            label_code.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            
            for j, b in enumerate(self.batches):
                var_id = (p['bakery_product_id'], b['id'])
                self.var_alloc[var_id] = tk.IntVar(value=p['bakery_allocation_batch_'+str(b['id'])+'_quantity'])
                
            label_ordered = ttk.Label(sbf.scrolled_frame, text=float(p['ordered_quantity']), width=4, anchor="e")
            label_ordered.grid(row=i, column=1, padx=5, pady=2, sticky="w")
            
            label_diff = ttk.Label(sbf.scrolled_frame, text=0, width=4, anchor="e")
            label_diff.grid(row=i, column=2, padx=5, pady=2, sticky="w")
                
            label_left_equal = ttk.Label(sbf.scrolled_frame, text='=', width=2, anchor='center')
            label_left_equal.grid(row=i, column=3, padx=5, pady=2, sticky="w")
            
            for j, b in enumerate(self.batches):
                var_id = (p['bakery_product_id'], b['id'])
                
                ve = ValueEntry(sbf.scrolled_frame, 
                                iid = p['bakery_product_id'],
                                width=5, 
                                textvariable=self.var_alloc[var_id])
                ve.grid(row=i, column=j+4, padx=2, pady=2, sticky="w")
                
                if processes[b['id']][p['bakery_product_id']] is None:
                    # ve.config(state='disabled')
                    ve.grid_forget()
                
                ve.bind('<Return>', 
                        self.compute_event)

                ve.bind('<FocusOut>', 
                        self.compute_event)
                
            label_right_equal = ttk.Label(sbf.scrolled_frame, text='=', width=2, anchor='center')
            label_right_equal.grid(row=i, column=4+len(self.batches)+1, padx=2, pady=2, sticky="ew")
            
            label_sum = ttk.Label(sbf.scrolled_frame, text=0, width=3, anchor="e")
            label_sum.grid(row=i, column=5+len(self.batches)+1, padx=2, pady=2, sticky="w")
            
            self.labels[p['bakery_product_id']] = [label_sum, 
                                                    label_diff, 
                                                    label_code,
                                                    label_ordered,
                                                    label_diff,
                                                    label_left_equal,
                                                    label_right_equal]
            
            if p['bakery_shape_id'] is not None:
                self.shapes_product_list[p['bakery_shape_id']].append(p['bakery_product_id'])
                    
            
            self.compute(p['bakery_product_id'])
            
        
    def compute_event(self, event):
        bakery_product_id = event.widget.iid
        self.compute(bakery_product_id)
        self.save()
    
    def compute(self, bakery_product_id):
        labels = self.labels[bakery_product_id]
        
        s = 0
        for b in self.batches:
            vi = (bakery_product_id, b['id'])
            s += self.var_alloc[vi].get()
        
        diff = float(s-float(labels[3].cget("text")))
        
        labels[0].config(text=s)
        labels[1].config(text=diff)
        
        if diff<0:
            [l.config(style='red.TLabel') for l in labels]
        elif diff==0:
            [l.config(style='green.TLabel') for l in labels]
        else:
            [l.config(style='blue.TLabel') for l in labels]
            
        # shape
        bakery_shape_id = self.products_dict[bakery_product_id]['bakery_shape_id']
        if bakery_shape_id is not None:
            shape_total = 0
            for b in self.batches:
                shape_sum = 0
                for p_id in self.shapes_product_list[bakery_shape_id]:
                    vi = (p_id, b['id'])
                    shape_sum += self.var_alloc[vi].get()
                self.shapes_labels[(b['id'], bakery_shape_id)].config(text=shape_sum)
                shape_total += shape_sum
            self.shapes_labels[('tot', bakery_shape_id)].config(text = shape_total)
                        
    
    def save(self):
        a = self.farm.bakery.allocation.get_entries(columns=['id', 'bakery_product_id', 'bakery_batch_id'],
                                                    where='sales_distribution_id='+str(self.sales_distribution_id),
                                                    list_dict=True)
        a_id = {(aa['bakery_product_id'], aa['bakery_batch_id']) : aa['id'] for aa in a}
        
        print(a_id)
        
        for p in self.products:
            for b in self.batches:
                var_id = (p['bakery_product_id'], b['id'])
                
                if var_id not in a_id.keys():
                    if self.var_alloc[var_id].get() > 0:
                        self.farm.bakery.allocation.insert_entry(sales_distribution_id=self.sales_distribution_id,
                                                                 bakery_product_id=p['bakery_product_id'],
                                                                 bakery_batch_id=b['id'],
                                                                 quantity=self.var_alloc[var_id].get())
                else:
                    if self.var_alloc[var_id].get() >= 0:
                        self.farm.bakery.allocation.update_entry(i=a_id[var_id],
                                                                 quantity=self.var_alloc[var_id].get())
        
    def generate(self, *event):
        distribution = self.farm.sales.distribution.get_entry(self.sales_distribution_id)
        
        path_prefix = timestamp_to_date(distribution['date'], date_format ='%Y-%m-%d')
        path_prefix +='_paille_'+self.farm.file_name+'_allocation'

        self.farm.bakery.allocation.report(sales_distribution_id=self.sales_distribution_id, 
                                           open_file=True, 
                                           path_prefix=path_prefix,
                                           debug_mode=False,
                                           clean=True)        
        