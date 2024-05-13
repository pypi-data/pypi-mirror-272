# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

class ValueEntry(ttk.Entry):
    def __init__(self, master, default=None, iid=None, **kwargs):
        if 'justify' not in kwargs.keys():
            kwargs['justify'] = 'right'
            
        ttk.Entry.__init__(self, master, **kwargs)
        
        self.default = default
        self.iid=iid
        
        