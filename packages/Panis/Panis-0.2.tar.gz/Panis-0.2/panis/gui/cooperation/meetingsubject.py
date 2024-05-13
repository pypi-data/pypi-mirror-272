# -*- coding: utf-8 -*-

# from ..widget import ComboboxDict, ValueEntry

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno


from ...farm import Farm
from ...table import timestamp_to_date, date_to_timestamp, today
import datetime 
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
# from widget import ComboboxDict, ValueEntry

from ..widget import ComboboxDict, ValueEntry

kinds = {1:{'name':'Information',
            'code':'I'},
         2:{'name':'Décision',
            'code':'D'},
         3:{'name':'Exploration',
            'code':'E'}}

state = {1:{'name':'À traiter',
             'color':'#c4d6f5',
             'selected_color':'#5b8ee3'},
          2:{'name':'en cours',
             'color':'#f7d394',
             'selected_color':'#eda932'},
          3:{'name':'clôt',
             'color':'#b7f59a',
             'selected_color':'#5bba2f'}}

state_inverse = {s['name'] : k for k, s in state.items()}

kinds_inverse = {kk['name'] : k for k, kk in kinds.items()}

class MeetingSubjectFrame(ttk.Frame):
    def __init__(self, master, farm:Farm):
        
        ttk.Frame.__init__(self, master)
        
        self.master = master
        self.farm = farm
        
        self.left_frame = LeftFrame(master=self, 
                                    farm=self.farm)
        self.left_frame.grid(row=0, column=0, sticky='ewn')
        
        self.right_frame = None
        
    def refresh_right_frame(self, meetingsubject_id=None):
        if self.right_frame is not None:
            self.right_frame.destroy()
            
        if meetingsubject_id is not None:
            self.right_frame = RightFrame(master=self,
                                          farm=self.farm, 
                                          meetingsubject_id=meetingsubject_id)
            self.right_frame.grid(row=0, column=1, sticky='wn')
        
class LeftFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, **args):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master, **args)
        
        self.meetingsubject_list_frame = MeetingSubjectListFrame(master=self, 
                                                     farm=self.farm)
        self.meetingsubject_list_frame.grid(row=0, column=0, pady=5, sticky='nw')
        
        # self.create_meetingsubject_label_frame = CreateMeetingSubjectLabelFrame(
            # master=self.master, 
            # farm=self.farm,
            # meetingsubject_list_frame=self.meetingsubject_list_frame)
        # self.create_meetingsubject_label_frame.grid(row=1, column=0, pady=5, sticky='nw')
    
        
class MeetingSubjectListFrame(ttk.Frame):
    
    def __init__(self, master, farm:Farm):
        
        self.farm = farm
        self.master = master
        
        ttk.Frame.__init__(self, master)
        
        header = ttk.Frame(self)
        header.grid(row=0, column=0, pady=5, columnspan=2, sticky='nwe')
        
        filtre_LF = ttk.LabelFrame(header, text="Filtres")
        filtre_LF.grid(row=0, column=0, sticky='w')
        
        self.filter = {}
        
        self.filter['next_agenda'] = tk.BooleanVar(value=0)
        
        for i, (k, v) in enumerate(state.items()):
            self.filter[('state', k)] = tk.BooleanVar(value=1)
            ttk.Checkbutton(filtre_LF, 
                            text=v['name'], 
                            variable=self.filter[('state', k)],
                            command=self.refresh)\
                .grid(sticky="w", row=0, column=i, pady=2, padx=5)
        
        ttk.Button(header, text="+", width=2, command=self.new)\
            .grid(row=0, column=1, padx=(10,0), sticky='e')
        
        date_filter_frame = ttk.Frame(filtre_LF)
        date_filter_frame.grid(row=1, columnspan=3, sticky="ew")
        
        ttk.Label(date_filter_frame, text="Filtrer par date d'édition :")\
            .grid(row=0, column=0, columnspan=3, padx=5)
        
        self.filter['date_operator'] = tk.StringVar(value='X')
        date_operator_cb = ttk.Combobox(date_filter_frame, 
                     values=['X','=','>=','<='],
                     state="readonly",
                     textvariable=self.filter['date_operator'],
                     width=3)
        date_operator_cb.grid(row=1, column=0, padx=(5,0), pady=2, sticky="w")
        
        date_operator_cb.bind("<<ComboboxSelected>>", self.date_operator_cb_selected)
        
        self.filter['date'] = tk.StringVar(value=timestamp_to_date(today()))
        self.date_filter_entry = ttk.Entry(date_filter_frame, 
                                           textvariable=self.filter['date'],
                                           width=10,
                                           state='disabled')
        self.date_filter_entry.grid(row=1, column=1, padx=(0,0), pady=2, sticky="w")
        
        self.date_filter_button = ttk.Button(date_filter_frame, 
                                             text="GO", 
                                             width=2, 
                                             command=self.refresh,
                                             state='disabled')
        self.date_filter_button.grid(row=1, column=2, padx=0, pady=2, sticky="w")
        
        # GOODS LIST
        # define columns
        columns = ('kind', 'name', 'deadline', 'next_agenda')
        
        self.tree = ttk.Treeview(self,
                                 columns=columns, 
                                 show='headings', 
                                 selectmode="browse",
                                 height=18)
        
        # define headings
        self.tree.heading('kind', text='', anchor=tk.W)
        self.tree.heading('name', text='name', anchor=tk.W)
        self.tree.heading('deadline', text='échéance', anchor=tk.W)
        self.tree.heading('next_agenda', text='ODJ', anchor=tk.W)
        
        self.tree.column('kind', width=15, anchor=tk.W)
        self.tree.column('name', width=250, anchor=tk.W)
        self.tree.column('deadline', width=70, anchor=tk.W)
        self.tree.column('next_agenda', width=15, anchor=tk.W)
        
        for s_id, s in state.items():
            self.tree.tag_configure(str(s_id), background=s['color'])
            self.tree.tag_configure('selected_'+str(s_id), background=s['selected_color'])
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        self.tree.grid(row=1, column=0, sticky='wns')
        
        # add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky='ens')
        
        next_agenda_LF = ttk.LabelFrame(self, text="Ordre du jour")
        next_agenda_LF.grid(row=3, column=0, columnspan=2, sticky="we")
        
        
        ttk.Checkbutton(next_agenda_LF, 
                        text="Filtrer", 
                        variable=self.filter['next_agenda'],
                        command=self.refresh)\
            .grid(sticky="w", row=0, column=0, pady=2, padx=5)
        
        self.next_agenda_duration_label = ttk.Label(next_agenda_LF, text="xxx")
        self.next_agenda_duration_label.grid(sticky="e", row=1, column=0, pady=2, padx=5)
        
        ttk.Button(next_agenda_LF, 
                   text="Réinitialiser", 
                   command=self.purge_next_agenda)\
            .grid(row=1, column=1, pady=2, padx=5, sticky="e")
        
        self.fill()
    
    def date_operator_cb_selected(self, *event):
        if self.filter['date_operator'].get() == 'X':
            self.date_filter_entry.config(state='disabled')
            self.date_filter_button.config(state='disabled')
            self.refresh()
        else:
            self.date_filter_entry.config(state='normal')
            self.date_filter_button.config(state='normal')
    
    def fill(self):
        
        
        
        state_list = []
        for s_id, s in state.items():
            if self.filter[('state', s_id)].get():
                state_list.append(str(s_id))
        
        meetingsubject = self.farm.cooperation.meetingsubject.get_filtered_entries(state_list=state_list,
                                                                                   next_agenda=self.filter['next_agenda'].get(),
                                                                                   log_date_operator=self.filter['date_operator'].get(),
                                                                                   log_date=date_to_timestamp(self.filter['date'].get()))
        
        # meetingsubject = self.farm.cooperation.meetingsubject.get_entries(columns=['id',
        #                                                                            'name', 
        #                                                                            'kind',
        #                                                                            'state',
        #                                                                            'deadline',
        #                                                                            'position',
        #                                                                            'duration',
        #                                                                            'next_agenda'], 
        #                                              order_by='state, deadline ASC, kind, name',
        #                                              where=where,
        #                                              pandas=True)
        
        self.states = {}
        for _, g in meetingsubject.iterrows():
            
            next_agenda_label = ''
            if g['next_agenda']:
                next_agenda_label = 'X'
            
            self.tree.insert('', 
                             tk.END,
                             g['id'], 
                             values=[kinds[g['kind']]['code'],
                                     g['name'], 
                                     timestamp_to_date(g['deadline']),
                                     next_agenda_label],
                             tags = (str(g['state']),))
            self.states[g['id']] = g['state']
        
        next_agenda_duration = meetingsubject.loc[meetingsubject['next_agenda']==1,'duration'].sum()
        next_agenda_duration_h = int(next_agenda_duration / 60)
        next_agenda_duration_m = next_agenda_duration % 60
        self.next_agenda_duration_label.configure(text="Durée estimée : "+str(next_agenda_duration_h).zfill(2)+"h"+str(next_agenda_duration_m).zfill(2))
    
    def refresh(self, item_id=None, destroy=True, focus=True):
        if self.master.master.right_frame is not None and destroy:
            self.master.master.right_frame.destroy()
        
        self.tree.delete(*self.tree.get_children())
        self.fill()
        
        if item_id is not None:
            if focus:
                self.tree.focus(item_id)
            self.tree.selection_set(item_id)
            
            if not focus:
                self.set_selected_tag(meetingsubject_id=item_id)
    
    def on_select(self, event):
        meetingsubject_id = self.tree.focus()
        if len(meetingsubject_id) > 0:
            meetingsubject_id = int(meetingsubject_id)
            print("you clicked on meetingsubject id", meetingsubject_id)
            
            self.master.master.refresh_right_frame(meetingsubject_id=meetingsubject_id)
            
            self.set_selected_tag(meetingsubject_id=meetingsubject_id)
            
        self.tree.selection_remove(*self.tree.selection())

    def set_selected_tag(self, meetingsubject_id):
        # remove tags
        for iid, s in self.states.items():
            self.tree.item(iid, tags=(str(s),))
        
        # add selected tag
        self.tree.item(meetingsubject_id, tags=('selected_'+str(self.states[meetingsubject_id]),))


    def purge_next_agenda(self, *event):
        if askyesno("Réinitialiser", "Êtes-vous-sûrs de vouloir réinitialiser l'ordre du jour ?"):
            self.farm.cooperation.meetingsubject.purge_next_agenda()
            
            self.refresh()

    def new(self):
        iid = self.farm.cooperation.meetingsubject.insert_entry(
            name = 'nouveau sujet',
            log = timestamp_to_date(today())+' : création du sujet',
            deadline=today())
        
        self.refresh(item_id=iid)
        
class CreateMeetingSubjectLabelFrame(ttk.LabelFrame):
    def __init__(self, master, farm, meetingsubject_list_frame=None):
        self.master = master
        self.farm = farm
        self.meetingsubject_list_frame = meetingsubject_list_frame
        
        ttk.LabelFrame.__init__(self, master, text="Nouveau")
                
        label_nom = ttk.Label(self, text="nom")
        label_nom.grid(sticky="W",row=0,column=0, padx=5, pady=5)
        
        self.new_name_value = tk.StringVar()
        ttk.Entry(self,
                  textvariable=self.new_name_value,
                  width=20)\
            .grid(row=1, column=0, padx=5, pady=5, sticky='w')
        
        button1 = ttk.Button(self, text = "Créer", command=self.new)
        button1.grid(sticky="W",row=1,column=1, padx=5, pady=5)
    
    def new(self):
        iid = self.farm.cooperation.meetingsubject.insert_entry(
            name = self.new_name_value.get(),
            log = timestamp_to_date(today())+' : création du sujet',
            deadline=today())
        
        if self.meetingsubject_list_frame is not None:
            self.meetingsubject_list_frame.refresh(item_id=iid)
        
        self.new_name_value.set('')

class RightFrame(ttk.Frame):
    def __init__(self, master, farm:Farm, meetingsubject_id, **args):
        ttk.Frame.__init__(self, master, **args)
        
        self.farm = farm
        self.meetingsubject_id = meetingsubject_id
        
        data = self.farm.cooperation.meetingsubject.get_entry(i=self.meetingsubject_id)
        
        self.var = {}
        self.var['name'] = tk.StringVar(value=data['name'])
        self.var['creator'] = tk.StringVar(value=data['creator'])
        self.var['deadline'] = tk.StringVar(value=timestamp_to_date(data['deadline']))
        self.var['log'] = tk.StringVar(value=data['log'])
        self.var['next_agenda'] = tk.BooleanVar(value=data['next_agenda'])
        self.var['duration'] = tk.IntVar(value=data['duration'])
        self.var['state'] = tk.StringVar(value=state[data['state']]['name'])
        self.var['kind'] = tk.StringVar(value=kinds[data['kind']]['name'])
        
        state_LF = ttk.LabelFrame(self, text="État")
        state_LF.grid(row=0, column=0, columnspan=5, padx=5, pady=2, sticky="we")
                
        for i_s, (k, s) in enumerate(state.items()):
            radio = ttk.Radiobutton(state_LF,
                                    text=s['name'], 
                                    variable=self.var['state'], 
                                    value=s['name'],
                                    command=self.save)
            radio.grid(sticky="w", row=0, column=i_s, pady=2, padx=5)
        
        kind_LF = ttk.LabelFrame(self, text="Type")
        kind_LF.grid(row=1, column=0, columnspan=5, padx=5, pady=2, sticky="we")
                
        for i_k, (k, kk) in enumerate(kinds.items()):
            radio = ttk.Radiobutton(kind_LF,
                                    text=kk['name'], 
                                    variable=self.var['kind'], 
                                    value=kk['name'],
                                    command=self.save)
            radio.grid(sticky="w", row=0, column=i_k, pady=2, padx=5)
        
        ttk.Checkbutton(self, 
                        text="à l'ordre du jour de la prochaine réunion",
                        variable=self.var['next_agenda'],
                        command=self.save)\
            .grid(sticky="w", row=2, column=0, columnspan=3, pady=2, padx=5)
        
        ttk.Label(self, text="nom")\
            .grid(row=4, column=0, padx=5, pady=2, sticky="w")
        name_entry = ttk.Entry(self, textvariable=self.var['name'])
        name_entry.grid(row=4, column=1, pady=2, sticky="we", columnspan=5)
        name_entry.bind('<Return>', 
                self.save)
        name_entry.bind('<FocusOut>', 
                self.save)
        name_entry.bind('<FocusIn>', 
                self.clear_name)
        
        ttk.Label(self, text="auteur")\
            .grid(row=5, column=0, padx=5, pady=2, sticky="w")
        creator_entry = ttk.Entry(self, textvariable=self.var['creator'], width=15)
        creator_entry.grid(row=5, column=1, pady=2, sticky="w")
        creator_entry.bind('<Return>', 
                self.save)
        creator_entry.bind('<FocusOut>', 
                self.save)
        
        ttk.Label(self, text="durée")\
            .grid(row=5, column=2, padx=5, pady=2, sticky="e")
        duration_entry = ttk.Spinbox(self, 
                                     textvariable=self.var['duration'],
                                     from_=0,
                                     to=500,
                                     wrap=False,
                                     increment=5,
                                     width=4)
        duration_entry.grid(row=5, column=3, pady=2, sticky="w")
        duration_entry.bind('<Return>', 
                self.save)
        duration_entry.bind('<FocusOut>', 
                self.save)
        ttk.Label(self, text='min')\
            .grid(row=5, column=4, padx=1, pady=2, sticky="w")
        
        ttk.Label(self, text="échéance")\
            .grid(row=6, column=0, padx=5, pady=2, sticky="w")
        deadline_entry = ttk.Entry(self, textvariable=self.var['deadline'], width=10)
        deadline_entry.grid(row=6, column=1, pady=2, sticky="w")
        deadline_entry.bind('<Return>', 
                self.save)
        deadline_entry.bind('<FocusOut>', 
                self.save)
        ttk.Label(self, text="(JJ/MM/AAAA)")\
            .grid(row=6, column=2, pady=2, sticky="w")
        
        ttk.Label(self, text="Notes")\
            .grid(row=7, column=0, padx=5, pady=2, columnspan=3, sticky="w")
        
        note_frame = ttk.Frame(self)
        note_frame.grid(row=8, column=0, columnspan=6, sticky="we", padx=5, pady=2)
        
        v=ttk.Scrollbar(note_frame, orient='vertical')
        v.grid(row=0, column=1, sticky='wns')
        
        self.var['note'] = tk.Text(note_frame, 
                                   height=22, 
                                    width=60,
                                   yscrollcommand=v.set)
        self.var['note'].grid(row=0, column=0, sticky='we', pady=2)
        
        v.config(command=self.var['note'].yview)
        
        self.var['note'].insert("end-1c",  data['note'])
        
        self.var['note'].bind('<FocusOut>', 
                self.save)
        
        self.var['note'].bind("<Control-Key-a>", self.select_all)
        self.var['note'].bind("<Control-Key-A>", self.select_all) # just in case caps lock is on

        
        ttk.Button(self, text="Supprimer ce sujet", command=self.delete)\
            .grid(row=9, column=2, columnspan=3, sticky="e", pady=20)
    
    def select_all(self, event):
        self.var['note'].tag_add(tk.SEL, "1.0", tk.END)
        self.var['note'].mark_set(tk.INSERT, "1.0")
        self.var['note'].see(tk.INSERT)
        return 'break'
    
    def clear_name(self, *args):
        if self.var['name'].get() == 'nouveau sujet':
            self.var['name'].set('')
    
    def save(self, *args):
        self.farm.cooperation.meetingsubject.update_entry(
                            i= self.meetingsubject_id,
                            name = self.var['name'].get(),
                            state = state_inverse[self.var['state'].get()],
                            kind = kinds_inverse[self.var['kind'].get()],
                            creator = self.var['creator'].get(),
                            deadline = date_to_timestamp(self.var['deadline'].get()),
                            next_agenda = int(self.var['next_agenda'].get()),
                            note = self.var['note'].get("1.0",'end-1c'),
                            duration = int(self.var['duration'].get()))
        
        # log update
        # it exists ?
        log_id = self.farm.cooperation.meetingsubjectlog.get_entries(columns=['id'],
                                                                     where='cooperation_meetingsubject_id='+str(self.meetingsubject_id)+' AND date='+str(today()))
        if len(log_id)==0:
            self.farm.cooperation.meetingsubjectlog.insert_entry(cooperation_meetingsubject_id=self.meetingsubject_id,
                                                                 date=today())
        
        # refresh
        self.master.left_frame.meetingsubject_list_frame.refresh(item_id=self.meetingsubject_id,
                                                                 destroy=False,
                                                                 focus=False)
    
    def delete(self, *args):
        if askyesno("Supprimer", "Êtes-vous-sûrs de vouloir supprimer \""+ self.var['name'].get() +"\" ?"):
            self.farm.cooperation.meetingsubject.delete_entry(i=self.meetingsubject_id)
            
            self.master.left_frame.meetingsubject_list_frame.refresh()
            self.master.refresh_right_frame()