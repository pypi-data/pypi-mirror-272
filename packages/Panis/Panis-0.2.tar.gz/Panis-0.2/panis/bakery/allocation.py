# -*- coding: utf-8 -*-

from ..table import Table, Column

from .allocation_report import BakingReport


import os
import sys
import subprocess
import datetime

import operator

import numpy as np

class Allocation(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'bakery_allocation'
        columns = [Column(name='id',
                          sql_type='INTEGER',
                          index=True),
                   Column(name='sales_distribution_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('sales_distribution', 'id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='bakery_product_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_product_id', 'id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='bakery_batch_id', 
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_batch_id', 'id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='quantity',
                          sql_type='INTEGER',
                          default=0.0)]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)
        
        
    def get_products(self, sales_distribution_id):
        
        batches = self.get_entries(columns=['id'], table_name='bakery_batch', list_dict=True)
            
        
        query = """
        SELECT 
        logistic_goods.id,
        logistic_goods.code,
        bakery_product.id,
        bakery_product.bakery_shape_id,
        CASE WHEN qu.ordered_quantity is NULL THEN 0 ELSE qu.ordered_quantity END,"""
        
        for b in batches:
            query += " alloc_batch_"+str(b['id'])+".id, "
            query += " CASE WHEN alloc_batch_"+str(b['id'])+".quantity IS NULL THEN 0 ELSE alloc_batch_"+str(b['id'])+".quantity END, "
        
        query +="""
        logistic_goods.unit
        FROM
        bakery_product
        LEFT JOIN
        logistic_goods
        ON
        bakery_product.logistic_goods_id = logistic_goods.id
        LEFT JOIN
        (
            SELECT
            sales_product.logistic_goods_id as id,
            SUM(CASE WHEN sales_product.quantity IS NULL THEN 0 ELSE sales_product.quantity END) as ordered_quantity
            FROM
            sales_order
            RIGHT JOIN
            sales_product
            ON
            sales_order.id = sales_product.sales_order_id
            WHERE
            sales_order.sales_distribution_id="""+str(sales_distribution_id)+"""
            GROUP BY
            sales_product.logistic_goods_id    
        ) as qu
        ON
        logistic_goods.id = qu.id
        """
        
        for b in batches:
            query +="""
            LEFT JOIN
            (
                SELECT
                bakery_allocation.id,
                bakery_allocation.bakery_product_id,
                bakery_allocation.quantity
                FROM
                bakery_allocation
                WHERE
                bakery_allocation.sales_distribution_id="""+str(sales_distribution_id)+"""
                AND
                bakery_allocation.bakery_batch_id="""+str(b['id'])+"""
            ) as alloc_batch_"""+str(b['id'])+"""
            ON bakery_product.id = alloc_batch_"""+str(b['id'])+""".bakery_product_id
            """
        
        query +="""
        ORDER BY
        logistic_goods.position DESC, logistic_goods.code
        """
        columns = ('logistic_goods_id',
                   'code',
                   'bakery_product_id',
                   'bakery_shape_id',
                   'ordered_quantity')
        
        for b in batches:
            columns += ('bakery_allocation_batch_'+str(b['id'])+'_id',)
            columns += ('bakery_allocation_batch_'+str(b['id'])+'_quantity',)
        
        columns += ('unit',)
        
        return self._tuples_dict(query=query, 
                                 columns=columns)
    
    def get_entry_by_data(self,
                          sales_distribution_id,
                          bakery_product_id,
                          bakery_batch_id):
        query = """
        SELECT
        id,
        quantity
        FROM
        bakery_allocation
        WHERE
        sales_distribution_id="""+str(sales_distribution_id)+"""
        AND
        bakery_product_id="""+str(bakery_product_id)+"""
        AND
        bakery_batch_id="""+str(bakery_batch_id)+"""
        LIMIT 1
        """
        
        columns = ('id', 'quantity')
        
        tup = self._tuples_dict(query, columns)
        if len(tup)>0:
            return tup[0]
        else:
            return False
    
    def get_dough_quantity(self,
                           sales_distribution_id,
                           bakery_batch_id):
        query = """
        SELECT 
        bakery_process.bakery_dough_id,
        bakery_dough.name,
        SUM(bakery_allocation.quantity * bakery_dough.baking_weight_loss_inverse * bakery_product.weight)
        FROM
        bakery_allocation
        LEFT JOIN
        bakery_process
        ON
        bakery_allocation.bakery_product_id = bakery_process.bakery_product_id
        AND
        bakery_allocation.bakery_batch_id = bakery_process.bakery_batch_id
        LEFT JOIN
        bakery_product
        ON
        bakery_allocation.bakery_product_id = bakery_product.id
        LEFT JOIN
        bakery_dough
        ON
        bakery_process.bakery_dough_id = bakery_dough.id
        WHERE
        bakery_allocation.sales_distribution_id="""+str(sales_distribution_id)+"""
        AND
        bakery_allocation.bakery_batch_id="""+str(bakery_batch_id)+"""
        GROUP BY
        bakery_process.bakery_dough_id
        """
        
        columns = ('bakery_dough_id',
                   'bakery_dough_name',
                   'quantity')
        
        tup_direct =  self._tuples_dict(query=query, 
                                 columns=columns)
        
        query = """
        SELECT
        bakery_recipe.bakery_dough_as_recipe_id,
        bakery_dough.name,
        SUM(bakery_allocation.quantity * bakery_recipe.quantity / bakery_recipe_sum.total_quantity * bakery_product.weight * bakery_dough.baking_weight_loss_inverse)
        FROM
        bakery_allocation
        LEFT JOIN
        bakery_process
        ON
        bakery_allocation.bakery_product_id = bakery_process.bakery_product_id
        AND
        bakery_allocation.bakery_batch_id = bakery_process.bakery_batch_id
        
        RIGHT JOIN
        bakery_recipe
        ON
        bakery_recipe.bakery_dough_id = bakery_process.bakery_dough_id
        
        LEFT JOIN
        bakery_product
        ON
        bakery_allocation.bakery_product_id = bakery_product.id
        
        LEFT JOIN
        bakery_dough
        ON
        bakery_recipe.bakery_dough_as_recipe_id = bakery_dough.id
        
        LEFT JOIN
        (
        SELECT
            bakery_recipe.bakery_dough_id,
            SUM(bakery_recipe.quantity) as total_quantity
            FROM
            bakery_recipe
            GROUP BY
            bakery_recipe.bakery_dough_id
        ) as bakery_recipe_sum
        ON
        bakery_process.bakery_dough_id = bakery_recipe_sum.bakery_dough_id
        
        WHERE
        bakery_allocation.sales_distribution_id="""+str(sales_distribution_id)+"""
        AND
        bakery_allocation.bakery_batch_id="""+str(bakery_batch_id)+"""
        AND
        bakery_recipe.bakery_dough_as_recipe_id IS NOT NULL
        GROUP BY
        bakery_recipe.bakery_dough_as_recipe_id
        """
        
        columns= ('bakery_dough_id',
                  'bakery_dough_name',
                  'quantity')
        
        tup_indirect = self._tuples_dict(query=query, columns=columns)
        
        tup_direct = {t['bakery_dough_id'] : t for t in tup_direct}
        tup_indirect = {t['bakery_dough_id'] : t for t in tup_indirect}
        
        ti_to_append = []
        
        for i, ti in tup_indirect.items():
            if i in tup_direct.keys():
                tup_direct[i]['quantity'] += ti['quantity']
            else:
                ti_to_append.append(ti)
        
        return list(tup_direct.values()) + ti_to_append
    
    def report(self, 
               sales_distribution_id, 
               open_file=False, 
               path_prefix=None,
               debug_mode=False,
               clean=True):
        br = BakingReport(farm=self.farm, 
                          sales_distribution_id=sales_distribution_id,
                          path_prefix=path_prefix,
                          debug_mode=debug_mode,
                          clean=clean)
        br.generate(open_file=open_file)
                