# -*- coding: utf-8 -*-

from ..table import Table, Column

class Goods(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'logistic_goods'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='name',
                          sql_type='TEXT',
                          default=''),
                   Column(name='code',
                          sql_type='TEXT',
                          default=''),
                   Column(name='unit',
                          sql_type='TEXT',
                          default=''),
                   Column(name='io',
                          sql_type='TEXT',
                          default='input'),
                   Column(name='position',
                          sql_type='REAL',
                          default=0.0),
                   Column(name='color',
                          sql_type='TEXT',
                          default=''),
                   Column(name='trigger_bakery',
                          sql_type='BOOLEAN',
                          default=0),
                   Column(name='trigger_mill',
                          sql_type='BOOLEAN',
                          default=0)
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
            
    def get_entries_from_sector(self,
                                sector,
                                columns=None,
                                io='both',
                                order_by='name',
                                desc=False):
        return self.get_entries_from_sectors(sectors=[sector],
                                             columns=columns,
                                             io=io,
                                             order_by=order_by,
                                             desc=desc)
    
    def get_entries_from_sectors(self, 
                                 sectors,
                                 columns=None,
                                 io='both', 
                                 order_by='name',
                                 desc=False):
        
        where = " AND ".join(["trigger_"+s+" = 1" for s in sectors])
        
        if io == 'input':
            where += " AND io <> 'output'"
        
        if io == 'output':
            where += " AND io <> 'input'"
        
        return self.get_entries(
            columns=columns,
            where=where,
            order_by=order_by,
            desc=desc)
        