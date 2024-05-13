# -*- coding: utf-8 -*-

from ..table import Table, Column

class Recipe(Table):
    def __init__(self, conn, farm):
        
        self.farm = farm
        
        name = 'bakery_recipe'
        columns = [Column(name='id', 
                          sql_type='INTEGER',
                          index=True),
                   Column(name='bakery_dough_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_dough','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='logistic_goods_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('logistic_goods','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='bakery_dough_as_recipe_id',
                          sql_type='INTEGER',
                          default='NULL',
                          references=('bakery_dough','id'),
                          on_update='CASCADE',
                          on_delete='CASCADE'),
                   Column(name='quantity', 
                          sql_type='REAL',
                          default=0.0)
                   ]
        
        Table.__init__(self, 
                       conn=conn, 
                       name=name,
                       columns=columns)

    def get_logistic_goods(self, bakery_dough_id):
        query="""SELECT 
                    bakery_recipe.id, 
                    logistic_goods.id as logistic_goods_id,
                    logistic_goods.name as logistic_goods_name,
                    bakery_recipe.quantity,
                    logistic_goods.unit as logistic_goods_unit
                    FROM
                    bakery_recipe
                    RIGHT JOIN
                    logistic_goods 
                    ON bakery_recipe.logistic_goods_id = logistic_goods.id
                    WHERE
                    bakery_recipe.bakery_dough_id = '"""+str(bakery_dough_id)+"""'
                    AND
                    bakery_recipe.bakery_dough_as_recipe_id IS NULL
                    ORDER BY logistic_goods_name"""
        
        columns = ['id', 
                   'logistic_goods_id',
                   'logistic_goods_name',
                   'quantity',
                   'logistic_goods_unit']    
        
        return self._tuples_dict(query=query, 
                                 columns=columns)

    def get_bakery_dough(self, bakery_dough_id):
        query="""SELECT 
                    bakery_recipe.id, 
                    bakery_dough.id as bakery_dough_id,
                    bakery_dough.name as bakery_dough_name,
                    bakery_recipe.quantity
                    FROM
                    bakery_recipe
                    RIGHT JOIN
                    bakery_dough 
                    ON bakery_recipe.bakery_dough_as_recipe_id = bakery_dough.id
                    WHERE
                    bakery_recipe.bakery_dough_id = '"""+str(bakery_dough_id)+"""'
                    AND
                    bakery_recipe.logistic_goods_id IS NULL
                    ORDER BY bakery_dough.position DESC, bakery_dough_name"""
        
        columns = ['id', 
                   'bakery_dough_id',
                   'bakery_dough_name',
                   'quantity']    
        
        return self._tuples_dict(query=query, 
                                 columns=columns)
    
    def get_sorted_entries(self):
        query = """
        SELECT
        bakery_recipe.id,
        bakery_recipe.bakery_dough_id,
        bakery_recipe.logistic_goods_id,
        bakery_recipe.bakery_dough_as_recipe_id,
        bakery_recipe.quantity
        FROM
        bakery_recipe
        LEFT JOIN
        logistic_goods
        ON bakery_recipe.logistic_goods_id = logistic_goods.id
        ORDER BY
        logistic_goods.position DESC, logistic_goods.name
        """
        
        columns = ('id', 
                   'bakery_dough_id',
                   'logistic_goods_id',
                   'bakery_dough_as_recipe_id',
                   'quantity')
        
        return self._tuples_dict(query=query, 
                                 columns=columns)
        