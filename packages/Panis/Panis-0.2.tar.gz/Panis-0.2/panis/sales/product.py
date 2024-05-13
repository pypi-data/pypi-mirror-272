# -*- coding: utf-8 -*-
from ..table import Table, Column

import pandas as pd

class Product(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'sales_product'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='sales_order_id',
                          sql_type='INT',
                          default='NULL',
                          references=('sales_order','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='logistic_goods_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('logistic_goods','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='quantity',
                          sql_type='REAL',
                          default=0)]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
    
    def get_orders_and_producs_by_distribution(self, 
                                               sales_distribution_id, 
                                               sheet=True):
        query = """
        SELECT
        sales_order.id,
        sales_delivery.id,
        sales_delivery.name,
        sales_delivery.position,
        sales_client.id,
        sales_client.name || ' ' || sales_client.first_name,
        sales_client.note
        FROM
        sales_order
        LEFT JOIN
        sales_delivery
        ON
        sales_order.sales_delivery_id = sales_delivery.id
        LEFT JOIN
        sales_client
        ON
        sales_order.sales_client_id = sales_client.id
        WHERE
        sales_order.sales_distribution_id = """+str(sales_distribution_id)+"""
        ORDER BY
        sales_delivery.position DESC, 
        sales_client.name
        """
        
        columns=['sales_order_id',
                 'sales_delivery_id',
                 'sales_delivery_name',
                 'sales_delivery_position',
                 'sales_client_id',
                 'sales_client_name',
                 'sales_client_note']
        
        orders = self._pandas(query=query, columns=columns)
        
        deliveries = self.farm.sales.delivery.get_entries(columns=['id',
                                                                   'name', 
                                                                   'position',
                                                                   'new_page',
                                                                   'unsold_line',
                                                                   'market_sheet',
                                                                   'note'],
                                                          order_by='position DESC',
                                                          pandas=True)
        deliveries.set_index('id', inplace=True)
        
        goods = self.farm.logistic.goods.get_entries(columns=['id',
                                                              'name',
                                                              'code',
                                                              'color',
                                                              'position'],
                                                              where="io<>'input'",
                                                              order_by='position DESC',
                                                              pandas=True)
        goods.set_index('id', inplace=True)
        
        for g_id, g in goods.iterrows():
            # adding goods columns in orders
            orders[g_id]=0.0
            
        for i_o, o in orders.iterrows():
            products = self.farm.sales.product.get_entries(columns=['logistic_goods_id',
                                                                    'quantity'],
                                                           where="sales_order_id="+str(o['sales_order_id']),
                                                           list_dict=True)
            for p in products:
                orders.loc[i_o, p['logistic_goods_id']] = p['quantity']
        
        # orders['sales_delivery_client_name'] = orders['sales_delivery_name']+' - '+orders['sales_client_name']
        
        # sort
        orders['sales_client_name_upper'] = orders['sales_client_name'].str.upper()
        orders.sort_values(by=['sales_delivery_position',
                               'sales_client_name_upper'],
                           ascending=[False, True])
        
        if sheet:
            orders = orders[['sales_client_name',
                             'sales_order_id',
                             'sales_delivery_name'] + [g_id for g_id, g in goods.iterrows()]]
        
        return orders, deliveries, goods
    
    def get_all_products(self, i):
        query = """
        SELECT 
        logistic_goods.id,
        logistic_goods.code,
        qu.id,
        CASE WHEN qu.quantity is NULL THEN 0 ELSE qu.quantity END,
        logistic_goods.unit,
        logistic_goods.trigger_bakery,
        logistic_goods.trigger_mill
        FROM
        logistic_goods
        LEFT JOIN
        (
            SELECT 
            id,
            logistic_goods_id,
            quantity
            FROM
            sales_product
            WHERE
            sales_order_id = """+str(i)+"""
        ) as qu
        ON
        qu.logistic_goods_id = logistic_goods.id
        WHERE
        logistic_goods.io <> 'input'
        ORDER BY
        logistic_goods.position DESC
        """
        columns = ('logistic_goods_id',
                   'code',
                   'sales_product_id',
                   'quantity',
                   'unit',
                   'trigger_bakery',
                   'trigger_mill')
        
        return self._tuples_dict(query=query, 
                                 columns=columns)
    
    def get_ordered_products(self, sales_distribution_id):
        query = """
        SELECT
        sales_order.logistic_goods_id,
        SUM(CASE WHEN sales_product.quantity IS NULL THEN 0 ELSE sales_product.quantity END)
        FROM
        sales_order
        RIGHT JOIN
        sales_product
        ON
        sales_order.id = sales_product.sales_order_id
        WHERE
        sales_order.sales_distribution_id="""+str(sales_distribution_id)+"""
        GROUP BY
        sales_order.logistic_goods_id
        """
        
        columns = ('logistic_goods_id',
                   'quantity')
        return self._tuples_dict(query=query, 
                                 columns=columns)
    

def pd_insert(df, i, values):
    line = pd.DataFrame(values, index=[i+1])
    return pd.concat([df.iloc[:i], line, df.iloc[i:]]).reset_index(drop=True)