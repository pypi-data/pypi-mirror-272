# -*- coding: utf-8 -*-

from ..table import Table, Column

class Batch(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'bakery_batch'
        columns = [Column(name='id', 
                          sql_type='INTEGER',
                          index=True),
                   Column(name='name',
                          sql_type='TEXT',
                          default=''),
                   Column(name='code',
                          sql_type='TEXT',
                          default=''),
                   Column(name='note',
                          sql_type='TEXT',
                          default=''),
                   Column(name='position', 
                          sql_type='REAL',
                          default=0.0)
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
    
    def get_used_batch(self):
        batch_cols = self.get_columns()
        batch_full_cols = ['bakery_batch.'+c for c in batch_cols]
        
        query = """
        SELECT """+', '.join(batch_full_cols)+""",
        COUNT(*) as count_batch
        FROM
        bakery_process
        LEFT JOIN
        bakery_batch
        ON
        bakery_process.bakery_batch_id = bakery_batch.id
        GROUP BY 
        bakery_process.bakery_batch_id
        """
        
        columns = tuple(batch_cols) + ('count_batch',)
        
        return self._tuples_dict(query=query, 
                                 columns=columns)