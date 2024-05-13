# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

class ComboboxDict(ttk.Combobox):

    def __init__(self, master, sort_values=False, none_value=None, **options):
        
        self.dict = None

        # get dictionary from options and put list of keys
        if 'values' in options:
            if isinstance(options.get('values'), dict):
                self.dict = options.get('values')
                keys = list(self.dict.keys())
                if sort_values:
                    keys = sorted(keys)
                if none_value is not None:
                    keys = [none_value] + keys
                    self.dict[none_value] = None
                options['values'] = keys
        
            self._values = options['values']
        
        self.inverse_dict = {v : k for k,v in self.dict.items()}
        
        # combobox constructor with list of keys
        ttk.Combobox.__init__(self, master, **options)
        
        self.bind('<KeyRelease>', self.check_input)

    # overwrite `get()` to return `value` instead of `key`
    def get(self):                              
        if self.dict:
            return self.dict[ttk.Combobox.get(self)]
        else:
            return ttk.Combobox.get(self)
    
    def set_id(self, i):
        self.set(self.inverse_dict[i])
    
    def set_value(self, value):
        self.set(value)
    
    def get_id(self):
        return self.dict[ttk.Combobox.get(self)]
        
    def get_value(self):
        return ttk.Combobox.get(self)
    
    
    def check_input(self, event):
        value = event.widget.get_value()
    
        if value == '':
            self['values'] = self._values
        else:
            data = []
            for item in self._values:
                if value.lower() in item.lower():
                    data.append(item)
    
            self['values'] = data
        
        # self.event_generate('<Button-1>')
        # self.after(0, self.focus_set)