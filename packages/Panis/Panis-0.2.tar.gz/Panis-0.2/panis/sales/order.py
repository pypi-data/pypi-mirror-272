# -*- coding: utf-8 -*-
from ..table import Table, Column

from .order_report import OrderReport

class Order(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'sales_order'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='sales_distribution_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('sales_distribution','id'),
                          on_update='CASCADE',
                          on_delete='SET DEFAULT'),
                   Column(name='sales_delivery_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('sales_delivery','id'),
                          on_update='CASCADE',
                          on_delete='SET DEFAULT'),
                   Column(name='sales_client_id',
                          sql_type='INTEGER',
                          references=('sales_client','id'),
                          on_update='CASCADE',
                          on_delete='SET DEFAULT'),
                   Column(name='note',
                          sql_type='TEXT',
                          default='')]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)

    def count_by_sales_distribution(self):
        query = """SELECT
            sales_distribution.id,
            sales_distribution.date, 
            CASE WHEN order_count.n IS NULL THEN 0 ELSE order_count.n END,
            CASE WHEN product_sum.p IS NULL THEN 0 ELSE product_sum.p END
            FROM
            sales_distribution
            LEFT JOIN
            (
                SELECT 
                sales_distribution_id, 
                COUNT(*) as n
                FROM
                sales_order
                GROUP BY 
                sales_distribution_id
            ) 
            as order_count
            ON sales_distribution.id = order_count.sales_distribution_id
            LEFT JOIN
            (
                SELECT
                sales_order.sales_distribution_id as id,
                SUM(sales_product.quantity) as p
                FROM
                sales_product
                LEFT JOIN
                sales_order
                ON
                sales_order.id = sales_product.sales_order_id
                GROUP BY 
                sales_order.sales_distribution_id
            ) as product_sum
            ON
            sales_distribution.id = product_sum.id
            ORDER BY
            sales_distribution.date DESC
        """
        columns = ('id', 'date', 'count_order', 'product_sum')
        
        return self._tuples_dict(query, columns=columns)
    
    def count_by_sales_delivery(self, sales_distribution_id):
        query = """SELECT
            sales_delivery.id,
            sales_delivery.name, 
            CASE WHEN order_count.n IS NULL THEN 0 ELSE order_count.n END,
            CASE WHEN product_sum.p IS NULL THEN 0 ELSE product_sum.p END
            FROM
            sales_delivery
            LEFT JOIN
            (
                SELECT 
                sales_delivery_id,
                COUNT(*) as n
                FROM
                sales_order
                WHERE
                sales_distribution_id="""+str(sales_distribution_id)+"""
                GROUP BY 
                sales_delivery_id
            ) 
            as order_count
            ON sales_delivery.id = order_count.sales_delivery_id
            LEFT JOIN
            (
                SELECT
                sales_order.sales_delivery_id as id,
                SUM(sales_product.quantity) as p
                FROM
                sales_product
                LEFT JOIN
                sales_order
                ON
                sales_order.id = sales_product.sales_order_id
                WHERE
                sales_order.sales_distribution_id="""+str(sales_distribution_id)+"""
                GROUP BY 
                sales_order.sales_delivery_id
            ) as product_sum
            ON
            sales_delivery.id = product_sum.id
            ORDER BY
            sales_delivery.position DESC, sales_delivery.name
        """
        columns = ('id', 'name', 'count_order', 'product_sum')
        
        
        return self._tuples_dict(query, columns=columns)
    
    def get_clients(self, 
                    sales_distribution_id,
                    sales_delivery_id):
        query = """
        SELECT 
        sales_order.id,
        sales_client.name || ' ' || sales_client.first_name as name,
        CASE WHEN product_sum.p IS NULL THEN 0 ELSE product_sum.p END
        FROM
        sales_order
        LEFT JOIN
        sales_client
        ON
        sales_order.sales_client_id = sales_client.id
        LEFT JOIN
        (
            SELECT
            sales_order.id as id,
            SUM(sales_product.quantity) as p
            FROM
            sales_product
            LEFT JOIN
            sales_order
            ON
            sales_order.id = sales_product.sales_order_id
            WHERE
            sales_order.sales_distribution_id = """+str(sales_distribution_id)+"""
            AND
            sales_order.sales_delivery_id = """+sales_delivery_id+"""
            GROUP BY 
            sales_order.id
        ) as product_sum
        ON
        sales_order.id = product_sum.id
        WHERE
        sales_distribution_id = """+str(sales_distribution_id)+"""
        AND
        sales_delivery_id = """+sales_delivery_id+"""
        ORDER BY
        name
        """
        columns = ('sales_order_id', 'name', 'p')
        
        return self._tuples_dict(query=query, columns=columns)
    
    def get_remaining_clients(self,
                              sales_distribution_id,
                              sales_delivery_id):
        query = """
        SELECT
        sales_client.id,
        sales_client.name || ' ' || sales_client.first_name as full_name
        FROM
        sales_client
        LEFT JOIN
        (
         SELECT
         sales_client_id,
         1 as trigger_ordered
         FROM
         sales_order
         WHERE
         sales_distribution_id = """+str(sales_distribution_id)+"""
         AND
         sales_delivery_id = """+str(sales_delivery_id)+"""
        ) as qu
        ON
        qu.sales_client_id = sales_client.id
        WHERE
        qu.trigger_ordered IS NULL
        ORDER BY full_name
        """
        columns = ('id', 'name')
        
        return self._tuples_dict(query=query, columns=columns)
    
    def report(self, 
               sales_distribution_id, 
               open_file=False, 
               path_prefix=None,
               debug_mode=False,
               clean=True):
        r = OrderReport(farm=self.farm, 
                        sales_distribution_id=sales_distribution_id,
                        path_prefix=path_prefix,
                        debug_mode=debug_mode,
                        clean=clean)
        r.generate(open_file=open_file)
    