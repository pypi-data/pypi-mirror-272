# -*- coding: utf-8 -*-

from ..table import Table, Column

class Product(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'bakery_product'
        
        columns = [Column(name='id', 
                          sql_type='INTEGER',
                          index=True),
                   Column(name='logistic_goods_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('logistic_goods','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='weight', 
                          sql_type='REAL',
                          default=0.0),
                   Column(name='bakery_shape_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_shape','id'),
                          on_update='CASCADE',
                          on_delete='SET DEFAULT'),
                   Column(name='extra_bakery_dough_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_dough','id'),
                          on_update='CASCADE',
                          on_delete='SET DEFAULT'),
        ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
    
    def create(self, return_logistic_goods_id=True, **data):
        
        if 'unit' not in data.keys():
            data['unit'] = 'u'
        
        logistic_goods_data = self._select_data(data=data,
                                                table_name='logistic_goods')
        bakery_product_data = self._select_data(data=data)
        
        
        logistic_goods_data['io'] = 'output'
        logistic_goods_data['trigger_bakery'] = True
        
        logistic_goods_id = self.insert_entry(table_name = 'logistic_goods',
                                              **logistic_goods_data)
        
        bakery_product_data['logistic_goods_id'] = logistic_goods_id
        print('>>>', bakery_product_data)
        bakery_product_id = self.insert_entry(**bakery_product_data)
        
        if return_logistic_goods_id:
            return logistic_goods_id
    
        return bakery_product_id
    
    # def populate_process(self, i):
    #     batch_list = self.get_entries(columns=['id'], 
    #                                   table_name="bakery_batch",
    #                                   list_dict=True)
    #     process_list = self.get_entries(columns=['id'],
    #                                   table_name="bakery_process",
    #                                   where="bakery_product_id="+str(i),
    #                                   list_dict=True)
        
    #     process_id_list = [pl['id'] for pl in process_list]
        
    #     for batch in batch_list:
    #         if batch['id'] not in process_id_list:
    #             self.insert_entry(table_name="bakery_process",
    #                               bakery_product_id=i,
    #                               bakery_batch_id=batch['id'])
    
    def get_entry_by_logistic_goods_id(self, 
                                       i, 
                                       columns=None, 
                                       force=False):
            """
            Parameters
            ----------
            table : str
                table name
            i : int
                entry index.
            columns : list(str), default=None
                list of column names. If None, "all columns" is set.

            Returns
            -------
            data : dict
                dict of data (keys are sql columns).

            """
            if columns is None:
                columns = self.get_columns()
            
            query = "SELECT "+", ".join(columns)
            query += " FROM "+self.name
            query += " WHERE logistic_goods_id="+str(i)
            query += " LIMIT 1"
            
            r = self._fetchone(query=query)
            
            if r is None:
                if force:
                    self.insert_entry(logistic_goods_id=i)
                    return self.get_entry_by_logistic_goods_id(i=i,
                                                               columns=columns,
                                                               force=False)
                else:
                    return None
            
            d = {c : r[i] for i, c in enumerate(columns)}
            
            return d
    