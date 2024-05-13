# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

from ...farm import Farm

# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from ..widget import ValueEntry

class ParameterFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        
        self.farm = farm
        
        parameters = self.farm.bakery.parameter.get_entry(i=1)
        
        self.vars = {}
        self.vars['extra_dough'] = tk.DoubleVar(value=parameters['extra_dough']*100)
        # self.vars['sourdough_king'] = tk.DoubleVar(value=parameters['sourdough_king'])
        
        ttk.Label(self, text="part de rab")\
            .grid(row=0, column=0, padx=2, pady=2, sticky="w")
        ValueEntry(self, default=1.0, width=4, textvariable=self.vars['extra_dough'])\
            .grid(row=0, column=1, padx=2, pady=2, sticky="w")
        ttk.Label(self, text="%")\
            .grid(row=0, column=2, pady=2, sticky="w")
            
        # ttk.Label(self, text="levain chef")\
            # .grid(row=1, column=0, padx=2, pady=2, sticky="w")
        # ValueEntry(self, default=1.0, width=4, textvariable=self.vars['sourdough_king'])\
            # .grid(row=1, column=1, padx=2, pady=2, sticky="w")
        # ttk.Label(self, text="kg")\
            # .grid(row=1, column=2, pady=2, sticky="w")
            
        ttk.Button(self, text="Enregistrer", command=self.save)\
            .grid(row=1, column=0, columnspan=3, sticky="w", padx=2, pady=10)
        
    def save(self, *event):
        self.farm.bakery.parameter.update_entry(i=1, 
                                                extra_dough=self.vars['extra_dough'].get()/100)