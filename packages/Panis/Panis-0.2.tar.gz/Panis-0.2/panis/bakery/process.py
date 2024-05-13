# -*- coding: utf-8 -*-

from ..table import Table, Column

class Process(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'bakery_process'
        columns = [Column(name='id', 
                          sql_type='INTEGER',
                          index=True),
                   Column(name='bakery_product_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_product','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='bakery_batch_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_batch','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='bakery_dough_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_dough','id'),
                          on_update='CASCADE',
                          on_delete='SET DEFAULT')
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
    
    # def get_entries_by_bakery_product_id(self, bakery_product_id):
    #         """
    #         Parameters
    #         ----------
    #         table : str
    #             table name
    #         i : int
    #             entry index.
    #         columns : list(str), default=None
    #             list of column names. If None, "all columns" is set.

    #         Returns
    #         -------
    #         data : dict
    #             dict of data (keys are sql columns).

    #         """
            
    #         query = """
    #             SELECT
    #             bakery_process.id,
    #             bakery_dough_id.bakery_product_id,
    #             bakery_process.bakery_batch_id,
    #             bakery_batch.code,
    #             bakery_process.bakery_dough_id
    #             FROM
    #             bakery_process
    #             LEFT JOIN
    #             bakery_batch
    #             ON
    #             bakery_process.bakery_batch_id = bakery_batch.id
    #             WHERE
    #             bakery_process.bakery_product_id = """+str(bakery_product_id)+"""
    #             ORDER BY
    #             bakery_batch.position DESC
    #         """
            
    #         columns = ('id',
    #                    'bakery_product_id', 
    #                    'bakery_batch_id',
    #                    'bakery_batch_code',
    #                    'bakery_dough_id')
    #         tup = self._tuples(query)
            
    #         return [{c : t[i] for i, c in enumerate(columns)} for t in tup]
    
    # def count_batch(self):
    #     query = """
    #     SELECT
    #     bakery_process.bakery_batch_id,
    #     COUNT(*)
    #     FROM bakery_process
    #     GROUP BY bakery_process.bakery_batch_id
    #     """
        
    #     columns = ('bakery_batch_id',
    #                'n')
        
    #     tup = self._tuples_dict(query=query, 
    #                             columns=columns)
        
    #     return {t['bakery_batch_id'] : t['n'] for t in tup}
    
    def get_dough_id_dict_product_id(self, bakery_batch_id):
        query = """
        SELECT
        bakery_product.id,
        bp.bakery_dough_id
        FROM
        bakery_product
        LEFT JOIN
        (
            SELECT
            bakery_process.bakery_product_id,
            bakery_process.bakery_dough_id
            FROM
            bakery_process
            WHERE
            bakery_process.bakery_batch_id = """+str(bakery_batch_id)+"""
        ) as bp
        ON bakery_product.id = bp.bakery_product_id
        """
        
        columns = ('bakery_product_id',
                   'bakery_dough_id')
        
        tup = self._tuples_dict(query=query, 
                                 columns=columns)
        
        return {t['bakery_product_id'] : t['bakery_dough_id'] for t in tup}