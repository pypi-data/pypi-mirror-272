# -*- coding: utf-8 -*-
from ..table import Table, Column

import datetime

class Distribution(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'sales_distribution'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='date',
                          sql_type='INTEGER',
                          default=''),
                   Column(name='note',
                          sql_type='TEXT',
                          default='')]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
    
    def insert_entry_as_human(self, date_format='%d/%m/%Y', **data):
        if 'date' in data.keys():
            int_date = datetime.datetime.strptime(data['date'], date_format).timestamp()
            data['date'] = int_date
        
        self.insert_entry(**data)
    
    def update_entry_as_human(self, date_format='%d/%m/%Y', **data):
        if 'date' in data.keys():
            int_date = datetime.datetime.strptime(data['date'], date_format).timestamp()
            data['date'] = int_date
        
        self.update_entry(**data)