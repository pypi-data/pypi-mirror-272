# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

class ScrollbarFrame(ttk.LabelFrame):
    """
    Extends class tk.Frame to support a scrollable Frame 
    This class is independent from the widgets to be scrolled and 
    can be used to replace a standard tk.Frame
    """
    def __init__(self, master, orient='vertical', **kwargs):
        ttk.LabelFrame.__init__(self, master, **kwargs)
        
        width = 100
        if 'width' in kwargs.keys():
            width = kwargs['width']
            
        height = 100
        if 'height' in kwargs.keys():
            height = kwargs['height']
        
        self.orient = orient
        
        if self.orient == 'vertical':
            # The Scrollbar, layout to the right
            self.vsb = ttk.Scrollbar(self, orient="vertical")
            self.vsb.pack(side="right", fill="y")
        elif self.orient == 'horizontal':
            # The Scrollbar, layout to the bottom
            self.vsb = ttk.Scrollbar(self, orient="horizontal")
            self.vsb.pack(side="bottom", fill="x")
        else:
            raise(ValueError("Unexpected orient argument. Expected 'vertical' or 'horizontal'."))

        # The Canvas which supports the Scrollbar Interface, layout to the left
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", width=width, height=height)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind the Scrollbar to the self.canvas Scrollbar Interface
        if self.orient == 'vertical':
            self.canvas.configure(yscrollcommand=self.vsb.set)
            self.vsb.configure(command=self.canvas.yview)
        else:
            self.canvas.configure(xscrollcommand=self.vsb.set)
            self.vsb.configure(command=self.canvas.xview)

        # The Frame to be scrolled, layout into the canvas
        # All widgets to be scrolled have to use this Frame as master
        self.scrolled_frame = tk.Frame(self.canvas, background=self.canvas.cget('bg'))
        self.canvas.create_window((4, 4), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self.on_configure)

        self.bind('<1>', self.self_focus)
        self.canvas.bind('<1>', self.self_focus)
        self.scrolled_frame.bind('<1>', self.self_focus)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            direction = 1
        if event.num == 4 or event.delta == 120:
            direction = -1
        
        if self.orient == 'vertical':
            self.canvas.yview_scroll(direction, "units")
        else:
            self.canvas.xview_scroll(direction, "units")

    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def self_focus(self, *event):
        self.focus_set()