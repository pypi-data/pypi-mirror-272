# -*- coding: utf-8 -*-


from ..table import timestamp_to_date
from ..report import LatexReport

import numpy as np
import pandas as pd

import math

class BakingReport(LatexReport):
    def __init__(self, 
                 farm, 
                 sales_distribution_id, 
                 debug_mode=False, 
                 **kwargs):
        self.sales_distribution_id = sales_distribution_id
        
        self.debug_mode=debug_mode
        
        distribution = farm.sales.distribution.get_entry(i=self.sales_distribution_id)
        distribution['human_date'] = timestamp_to_date(distribution['date'])
        
        LatexReport.__init__(self, 
                             farm, 
                             title = 'Distribution du '+distribution['human_date'],
                             sector='Fournil LHF',
                             font_size=11,
                             **kwargs)
    
    def _get_product_data(self):
        df = self.farm.bakery.allocation.get_entries(
                columns = ['bakery_product_id', 'bakery_batch_id', 'quantity'],
                where='sales_distribution_id='+str(self.sales_distribution_id),
                pandas=True)
        df.columns = ['bakery_product_id', 'bakery_batch_id', 'bakery_allocation_quantity']
        
        # product 
        df_product = self.farm.bakery.product.get_entries(columns=['id',
                                                                   'logistic_goods_id',
                                                                   'weight',
                                                                   'bakery_shape_id'],
                                                          pandas=True)
        df_product.columns = ['bakery_product_id',
                              'logistic_goods_id',
                              'bakery_product_weight',
                              'bakery_shape_id']
        
        df = df.merge(df_product,
                     left_on='bakery_product_id',
                     right_on='bakery_product_id',
                     how='left')
        
        df_product_sum = df[['bakery_product_id',
                             'bakery_batch_id',
                             'bakery_allocation_quantity']].groupby(['bakery_product_id',
                                                   'bakery_batch_id']).sum().reset_index()
        df_product_sum = df_product_sum.merge(df_product,
                                      on='bakery_product_id',
                                      how='inner')
        
        # goods
        df_goods = self.farm.logistic.goods.get_entries(columns=['id',
                                                                  'name',
                                                                  'code',
                                                                  'unit',
                                                                  'color',
                                                                  'position'],
                                                        pandas=True)
        df_goods.columns = ['logistic_goods_id',
                            'logistic_goods_name',
                            'logistic_goods_code',
                            'logistic_goods_unit',
                            'logistic_goods_color',
                            'logistic_goods_position']
        
        
        # batch
        df_batch = self.farm.bakery.batch.get_entries(columns=['id',
                                                               'name',
                                                               'code',
                                                               'position'],
                                                        pandas=True)
        
        list_batches = list(df_product_sum[['bakery_batch_id']].drop_duplicates().values[:,0])
        list_products = list(df_product_sum[['bakery_product_id']].drop_duplicates().values[:,0])
        
        a = np.zeros((len(list_products), len(list_batches)))
        
        for _, row in df_product_sum.iterrows():
            i = list_products.index(row['bakery_product_id'])
            j = list_batches.index(row['bakery_batch_id'])
            a[i,j] = row['bakery_allocation_quantity']
        
        df_product_data = pd.DataFrame(a)   
        df_product_data.columns = list_batches
        
        df_product_data['bakery_product_id'] = list_products
        
        df_product_data = df_product_data.merge(df_product,
                                                on='bakery_product_id',
                                                how='inner')
        
        df_product_data = df_product_data.merge(df_goods,
                                                on='logistic_goods_id',
                                                how='inner')
        
        # retirer batch non untilisé
        df_batch = df_batch.merge(df_product_sum[['bakery_batch_id']].drop_duplicates(),
                                  left_on='id',
                                  right_on='bakery_batch_id',
                                  how='inner')
        
        return df_product_data, df_batch
    
    def _get_dough_by_product(self):
        df_product_data, df_batch = self._get_product_data()
        
        df_process = self.farm.bakery.process.get_entries(columns=['bakery_product_id',
                                                                   'bakery_batch_id',
                                                                   'bakery_dough_id'],
                                                          pandas=True)
        
        
        df_dough = self.farm.bakery.dough.get_entries(columns=['id',
                                                               'name',
                                                               'baking_weight_loss_inverse',
                                                               'extra_dough'],
                                                      pandas=True)
           
        parameter = self.farm.bakery.parameter.get_entry(1)
        
        
        for i_b, b in df_batch.iterrows():
            df_process.columns = ['bakery_product_id',
                                  'bakery_batch_id',
                                  'bakery_dough_id_'+str(b['id'])]
            
            df_product_data = df_product_data.merge(df_process.loc[df_process['bakery_batch_id']==b['id'],
                                                                   ['bakery_product_id',
                                                                    'bakery_dough_id_'+str(b['id'])]],
                                                    on=['bakery_product_id'],
                                                    how='left')
            
            df_dough.columns = ['bakery_dough_id_'+str(b['id']),
                                'bakery_dough_name_'+str(b['id']),
                                'bakery_dough_baking_weight_loss_inverse_'+str(b['id']),
                                'extra_dough_'+str(b['id'])]
            df_product_data = df_product_data.merge(df_dough,
                                                    on=['bakery_dough_id_'+str(b['id'])],
                                                    how='left')
        
            df_product_data['bakery_dough_q_'+str(b['id'])] = \
                df_product_data[b['id']] \
                * df_product_data['bakery_product_weight'] \
                * df_product_data['bakery_dough_baking_weight_loss_inverse_'+str(b['id'])] \
                * (1 + df_product_data['extra_dough_'+str(b['id'])])
                # * (1 + parameter['extra_dough'])
                
        
        return df_product_data, df_batch
        
        
        # dough
        # 
        
        
        # df_product_data = df_product_data.merge(df_dough[['bakery_dough_id',
        #                                                   'bakery_dough_baking_weight_loss_inverse',
        #                                                   'bakery_dough_sourdough',
        #                                                   'bakery_dough_old_sourdough']],
        #                                         left_on='bakery_dough_id',
        #                                         right_on='bakery_dough_id',
        #                                         how='inner')
        
        # df_product_data = 
    
    def _get_shape_data(self):
        df = self.farm.bakery.allocation.get_entries(
                columns = ['bakery_product_id', 'bakery_batch_id', 'quantity'],
                where='sales_distribution_id='+str(self.sales_distribution_id),
                pandas=True)
        df.columns = ['bakery_product_id', 'bakery_batch_id', 'bakery_allocation_quantity']
        
        # product 
        df_product = self.farm.bakery.product.get_entries(columns=['id',
                                                                   'logistic_goods_id',
                                                                   'weight',
                                                                   'bakery_shape_id'],
                                                          pandas=True)
        df_product.columns = ['bakery_product_id',
                              'logistic_goods_id',
                              'bakery_product_weight',
                              'bakery_shape_id']
        
        df = df.merge(df_product,
                     left_on='bakery_product_id',
                     right_on='bakery_product_id',
                     how='left')
        
        df_shape = self.farm.bakery.shape.get_entries(columns=['id',
                                                               'name',
                                                               'code',
                                                               'position'],
                                                      pandas=True)
        df_shape.columns = ['bakery_shape_id',
                            'bakery_shape_name',
                            'bakery_shape_code',
                            'bakery_shape_position']
        
        df_shape_sum = df[['bakery_shape_id', 
                           'bakery_batch_id',
                           'bakery_allocation_quantity']]\
            .groupby(['bakery_shape_id',
                      'bakery_batch_id']).sum().reset_index()
        
        df_shape_sum = df_shape_sum.merge(df_shape,
                                          on='bakery_shape_id',
                                          how='left')
        
        
        list_batches = list(df_shape_sum[['bakery_batch_id']].drop_duplicates().values[:,0])
        list_shapes = list(df_shape_sum[['bakery_shape_id']].drop_duplicates().values[:,0])
        
        a = np.zeros((len(list_shapes), len(list_batches)))
        
        for _, row in df_shape_sum.iterrows():
            i = list_shapes.index(row['bakery_shape_id'])
            j = list_batches.index(row['bakery_batch_id'])
            a[i,j] = row['bakery_allocation_quantity']
        
        df_shape_data = pd.DataFrame(a)   
        df_shape_data.columns = list_batches
        
        df_shape_data['bakery_shape_id'] = list_shapes
        
        df_shape_data = df_shape_data.merge(df_shape,
                                            on='bakery_shape_id',
                                            how='inner')
        
        # batch
        df_batch = self.farm.bakery.batch.get_entries(columns=['id',
                                                               'name',
                                                               'code',
                                                               'position'],
                                                        pandas=True)
        
        # retirer batch non untilisé
        df_batch = df_batch.merge(df_shape_sum[['bakery_batch_id']].drop_duplicates(),
                                  left_on='id',
                                  right_on='bakery_batch_id',
                                  how='inner')
        
        return df_shape_data, df_batch
    
    def _get_recipe_data(self):
        # batch
        df_batch = self.farm.bakery.batch.get_entries(columns=['id',
                                                               'name',
                                                               'code',
                                                               'position'],
                                                        pandas=True)
        # sourdough_as_batch_id = -1
        # df_batch.loc[len(df_batch.index)] = [sourdough_as_batch_id,
                                         # 'Levains',
                                         # 'L',
                                         # -1]
        
        df = self.farm.bakery.allocation.get_entries(
                columns = ['bakery_product_id', 
                           'bakery_batch_id', 
                           'quantity'],
                where='sales_distribution_id='+str(self.sales_distribution_id),
                pandas=True)
        df.columns = ['bakery_product_id', 
                      'bakery_batch_id', 
                      'bakery_allocation_quantity']
        
        # product 
        df_product = self.farm.bakery.product.get_entries(columns=['id',
                                                                   'logistic_goods_id',
                                                                   'weight'],
                                                          pandas=True)
        df_product.columns = ['bakery_product_id',
                              'logistic_goods_id',
                              'bakery_product_weight']
        
        df = df.merge(df_product[['bakery_product_id', 'bakery_product_weight']],
                     left_on='bakery_product_id',
                     right_on='bakery_product_id',
                     how='left')
        
        # process
        df_process = self.farm.bakery.process.get_entries(columns=['id',
                                                                   'bakery_product_id',
                                                                   'bakery_batch_id',
                                                                   'bakery_dough_id'],
                                                          pandas=True)
        df_process.columns = ['bakery_process_id',
                              'bakery_product_id',
                              'bakery_batch_id',
                              'bakery_dough_id']
        df = df.merge(df_process,
                     on=['bakery_product_id', 
                         'bakery_batch_id'],
                     how='inner')
        
        # on retire ce qui ne sert plus
        # df.drop('bakery_product_id', axis=1, inplace=True)
        
        # dough
        df_dough = self.farm.bakery.dough.get_entries(columns=['id',
                                                               'name',
                                                               'baking_weight_loss_inverse',
                                                               'sourdough',
                                                               'old_sourdough',
                                                               'king_sourdough_weight',
                                                               'extra_dough',
                                                               'position'],
                                                      pandas=True)
        df_dough.columns = ['bakery_dough_id', 
                            'bakery_dough_name',
                            'bakery_dough_baking_weight_loss_inverse',
                            'bakery_dough_sourdough',
                            'bakery_dough_old_sourdough',
                            'bakery_dough_king_sourdough_weight',
                            'bakery_dough_extra_dough',
                            'bakery_dough_position']
        
        df = df.merge(df_dough[['bakery_dough_id',
                                'bakery_dough_baking_weight_loss_inverse',
                                'bakery_dough_sourdough',
                                'bakery_dough_old_sourdough',
                                'bakery_dough_extra_dough']],
                      left_on='bakery_dough_id',
                      right_on='bakery_dough_id',
                      how='inner')
        
        # on ajoute le levain chef
        df_sourdough = df_dough.loc[df_dough['bakery_dough_sourdough']==1]

        for i_r, sd in df_sourdough.iterrows():
            sourdough_to_add = {
                'bakery_product_id':None, 
                'bakery_batch_id':df_batch['id'].min(),
                'bakery_allocation_quantity':1, 
                'bakery_product_weight':sd['bakery_dough_king_sourdough_weight'], 
                'bakery_process_id':None, 
                'bakery_dough_id':sd['bakery_dough_id'], 
                'bakery_dough_baking_weight_loss_inverse':1, # il ne passe pas au four !! 
                'bakery_dough_sourdough':1,
                'bakery_dough_old_sourdough':1,
                'bakery_dough_extra_dough':0.01}
            
            df.loc[len(df.index)] = list(sourdough_to_add.values())
        
        
        
        # recipe
        df_recipe = self.farm.bakery.recipe.get_entries(columns=['id',
                                                                 'bakery_dough_id',
                                                                 'logistic_goods_id',
                                                                 'bakery_dough_as_recipe_id',
                                                                 'quantity'],
                                                        pandas=True)
        df_recipe.columns = ['bakery_recipe_id',
                             'bakery_dough_id',
                             'logistic_goods_id',
                             'bakery_dough_as_recipe_id',
                             'bakery_recipe_quantity']
        
        df_recipe_sum = df_recipe[['bakery_dough_id', 'bakery_recipe_quantity']].groupby(['bakery_dough_id']).sum().reset_index()
        df_recipe_sum.columns = ['bakery_dough_id', 'bakery_recipe_quantity_sum']
        df_recipe = df_recipe.merge(df_recipe_sum,
                                    on='bakery_dough_id',
                                    how='left')
        
        
        df_recipe['bakery_recipe_quantity_percent'] = df_recipe['bakery_recipe_quantity'] / df_recipe['bakery_recipe_quantity_sum']
        
        df_recipe = df_recipe[['bakery_recipe_id',
                               'bakery_dough_id',
                               'logistic_goods_id',
                               'bakery_dough_as_recipe_id',
                               'bakery_recipe_quantity_percent']]
        
        df_recipe['bakery_recipe_level'] = 0
    
        df = df.merge(df_recipe,
                      left_on='bakery_dough_id',
                      right_on='bakery_dough_id',
                      how='inner')
        
        parameter = self.farm.bakery.parameter.get_entry(1)
        
        
        df['q'] = df['bakery_allocation_quantity']\
                * df['bakery_product_weight']\
                * df['bakery_dough_baking_weight_loss_inverse']\
                * df['bakery_recipe_quantity_percent']\
                * (1 + df['bakery_dough_extra_dough'])
                # * (1 + parameter['extra_dough'])
        
        df = df[['bakery_batch_id', 
                'bakery_dough_id', 
                'bakery_dough_sourdough', 
                'bakery_dough_old_sourdough', 
                'logistic_goods_id', 
                'bakery_dough_as_recipe_id', 
                'bakery_recipe_quantity_percent', 
                'bakery_recipe_level', 
                'q']]
        
        self._recursive_recipe(df=df, df_recipe=df_recipe, df_dough=df_dough)
        
        # on calcule le poids de pâtes.
        df_dough_sum = df[['bakery_batch_id', 
                           'bakery_dough_id', 
                           'q']]\
            .groupby(['bakery_batch_id',
                      'bakery_dough_id']).sum().reset_index()
        
        df_dough_sum = df_dough_sum.merge(df_dough,
                                          on='bakery_dough_id',
                                          how='inner')
        
        # on amalgame tous les levains à un batch unique batch
        for i_r, sd in df_sourdough.iterrows():
            df.loc[df['bakery_dough_as_recipe_id']==sd['bakery_dough_id'], 'bakery_batch_id'] = df_batch['id'].min()
        
        # on agglomère les ingrédients
        df_recipe = df[['bakery_batch_id', 
                      'bakery_dough_id',
                      'bakery_dough_old_sourdough',
                      'logistic_goods_id',
                      'bakery_dough_as_recipe_id',
                      'q']]\
            .groupby(['bakery_batch_id', 
                      'bakery_dough_id',
                      'bakery_dough_old_sourdough',
                      'logistic_goods_id',
                      'bakery_dough_as_recipe_id'], 
                     dropna=False).sum().reset_index()
        
        # goods for product
        df_goods = self.farm.logistic.goods.get_entries(columns=['id',
                                                                  'name',
                                                                  'code',
                                                                  'unit',
                                                                  'position'],
                                                        pandas=True)
        df_goods.columns = ['logistic_goods_id',
                            'logistic_goods_name',
                            'logistic_goods_code',
                            'logistic_goods_unit',
                            'logistic_goods_position']
        
        df_recipe = df_recipe.merge(df_goods,
                              on='logistic_goods_id',
                              how='left')
        
        df_dough_for_recipe_merge = df_dough[['bakery_dough_id',
                                              'bakery_dough_name',
                                              'bakery_dough_sourdough',
                                              'bakery_dough_position']]
        df_dough_for_recipe_merge.columns = ['bakery_dough_as_recipe_id',
                                             'bakery_dough_as_recipe_name',
                                             'bakery_dough_as_recipe_sourdough',
                                             'bakery_dough_as_recipe_position']
        
        df_recipe = df_recipe.merge(df_dough_for_recipe_merge,
                                    on='bakery_dough_as_recipe_id',
                                    how='left')
        
        # retirer batch non utilisé
        df_batch = df_batch.merge(df_dough_sum[['bakery_batch_id']].drop_duplicates(),
                                  left_on='id',
                                  right_on='bakery_batch_id',
                                  how='inner')
        
        return df_recipe, df_dough_sum, df_batch
    
    def _recursive_recipe(self, df, df_recipe, df_dough, level=0):
        df_copy = df.copy()
        
        df_copy_width_dough_as_recipe = df_copy.loc[(df_copy['bakery_dough_as_recipe_id'].notnull())\
                                                      &(df_copy['bakery_recipe_level']==level)]
        # print(df_copy_width_dough_as_recipe)
        if len(df_copy_width_dough_as_recipe.index)>0:
            
            for index, row_df in df_copy_width_dough_as_recipe.iterrows():
                dough_as_recipe = df_dough.loc[df_dough['bakery_dough_id'] == row_df['bakery_dough_as_recipe_id']].reset_index().loc[0]
                
                # on vérifie si c'est pas du vieux levain
                if not (dough_as_recipe['bakery_dough_sourdough'] and row_df['bakery_dough_old_sourdough']):
                
                    bakery_dough_sourdough = dough_as_recipe['bakery_dough_sourdough']
                    bakery_dough_old_sourdough = dough_as_recipe['bakery_dough_old_sourdough']
                    
                    df_recipe_selected = df_recipe.loc[df_recipe['bakery_dough_id'] == row_df['bakery_dough_as_recipe_id']]
                    # print(row_df['bakery_dough_as_recipe_id'], len(df_recipe_selected.index))
                    
                    for _, row_df_recipe in df_recipe_selected.iterrows():
                        full_columns = df.columns.to_list()
                        # print(full_columns)
                        full_values = row_df.values
                        full_dict = {full_columns[i] : full_values[i] for i in range(len(full_columns))}
                        
                        # full_dict = {}
                        full_dict['bakery_batch_id'] = row_df['bakery_batch_id']
                        full_dict['bakery_dough_id'] = row_df['bakery_dough_as_recipe_id']
                        full_dict['bakery_dough_sourdough'] = bakery_dough_sourdough
                        full_dict['bakery_dough_old_sourdough'] = bakery_dough_old_sourdough
                        full_dict['logistic_goods_id'] = row_df_recipe['logistic_goods_id']
                        full_dict['bakery_dough_as_recipe_id'] = row_df_recipe['bakery_dough_as_recipe_id']
                        full_dict['bakery_recipe_quantity_percent'] = row_df_recipe['bakery_recipe_quantity_percent'] * row_df['bakery_recipe_quantity_percent']
                        full_dict['bakery_recipe_level'] = level + 1
                        full_dict['q'] = row_df['q'] * row_df_recipe['bakery_recipe_quantity_percent']
                        
                        df.loc[len(df.index)] = list(full_dict.values())
                    
            self._recursive_recipe(df,
                                   df_recipe=df_recipe,
                                   df_dough=df_dough,
                                   level=level+1)
    
    def _get_goods_data(self):
        df_recipe, df_dough_sum, df_batch = self._get_recipe_data()
        
        df_recipe_selected = df_recipe[['bakery_batch_id',
                              'bakery_dough_id',
                              'bakery_dough_old_sourdough',
                              'logistic_goods_id',
                              'bakery_dough_as_recipe_id',
                              'q']]
        
        df_goods_by_dough_sum = df_recipe_selected.groupby(
            ['bakery_batch_id',
            'bakery_dough_old_sourdough',
            'bakery_dough_id',
            'logistic_goods_id',
            'bakery_dough_as_recipe_id'],
            dropna=False).sum().reset_index()
        
        df_goods_by_dough_sum.loc[(df_goods_by_dough_sum['bakery_dough_old_sourdough']==1)\
                                  & (np.isnan(df_goods_by_dough_sum['bakery_dough_as_recipe_id'])), 'bakery_dough_old_sourdough'] = 0
        
        df_goods_sum = df_goods_by_dough_sum[['bakery_dough_old_sourdough',
                                              'logistic_goods_id',
                                              'bakery_dough_as_recipe_id',
                                              'q']]\
            .groupby(['bakery_dough_old_sourdough',
                      'logistic_goods_id',
                      'bakery_dough_as_recipe_id'],
                     dropna=False).sum().reset_index()
        
        df_goods = self.farm.logistic.goods.get_entries(columns=['id',
                                                                  'name',
                                                                  'code',
                                                                  'unit',
                                                                  'position'],
                                                        pandas=True)
        df_goods.columns = ['logistic_goods_id',
                            'logistic_goods_name',
                            'logistic_goods_code',
                            'logistic_goods_unit',
                            'logistic_goods_position']
        
        df_dough = self.farm.bakery.dough.get_entries(columns=['id',
                                                                'name',
                                                                'sourdough',
                                                                'position'],
                                                      pandas=True)
        df_dough_for_df_goods_by_dough_sum  = df_dough[['id',
                                                        'name',
                                                        'position']]
        df_dough_for_df_goods_by_dough_sum.columns = ['bakery_dough_id',
                                                      'bakery_dough_name',
                                                      'bakery_dough_position']
        
        df_goods_by_dough_sum = df_goods_by_dough_sum.merge(df_dough_for_df_goods_by_dough_sum,
                                    on='bakery_dough_id',
                                    how='left')
        
        df_goods_sum = df_goods_sum.merge(df_goods,
                                           on='logistic_goods_id',
                                           how='left')
        
        df_dough_for_df_goods_sum  = df_dough[['id',
                                                'name',
                                                'sourdough',
                                                'position']]
        df_dough_for_df_goods_sum.columns = ['bakery_dough_as_recipe_id',
                                              'bakery_dough_as_recipe_name',
                                              'bakery_dough_as_recipe_sourdough',
                                              'bakery_dough_as_recipe_position']
        
        
        df_goods_sum = df_goods_sum.merge(df_dough_for_df_goods_sum,
                                    on='bakery_dough_as_recipe_id',
                                    how='left')
        
        return df_goods_by_dough_sum, df_goods_sum
    
    def _inner_latex_content_product(self):
        df_product_data, df_batch = self._get_product_data()
        
        df_batch.sort_values(by='position',
                             ascending=False,
                             inplace=True)
        
        df_product_data.sort_values(by='logistic_goods_position',
                                    ascending=False,
                                    inplace=True)
        
        df_product_data = df_product_data.reset_index()
        
        
        latex = """
        \\section*{Produits}
        \\noindent\\begin{longtable}[l]{@{}L{1.6cm}"""+'R{0.7cm}'.join(['' for i in range(df_batch.index.size+1)])+"""R{0.7cm}@{}}
        """
        
        latex += " "
        for _, b in df_batch.iterrows():
            latex += " &\\textbf{"+b['code']+"}"
        latex += "& \\textbf{tot.} \\\\ \\hline \n"
        latex += "\\endhead \n"
        
        for i_r, p in df_product_data.iterrows():
            if len(p['logistic_goods_color'])>0:
                latex += "\\rowcolor{"+p['logistic_goods_color'][1:]+"}"
            elif i_r % 2 == 1:
                latex += "\\rowcolor{lightgray}"
            # if i_r % 2 == 1:
                # latex += "\\rowcolor{lightgray} "
            
            latex += p['logistic_goods_code']
            q_tot = 0
            for _, b in df_batch.iterrows():
                if not math.isnan(p[b['id']]):
                    latex += " & "+str(int(p[b['id']]))
                    q_tot += p[b['id']]
                else:
                    latex += " & "
                
            latex += " & " + str(int(q_tot)) + "\\\\ \n"
        
        latex += """
        \\end{longtable}
        """
        
        return latex   

    def _inner_latex_content_shape(self):
        df_shape_data, df_batch = self._get_shape_data()
        
        df_batch.sort_values(by='position',
                             ascending=False,
                             inplace=True)
        
        df_shape_data.sort_values(by='bakery_shape_position',
                                    ascending=False,
                                    inplace=True)
        
        latex = """
        \\section*{Formats}
        \\noindent\\begin{longtable}[l]{L{1cm}"""+'R{0.7cm}'.join(['' for i in range(df_batch.index.size+1)])+"""R{0.7cm}}
        """
        
        latex += " "
        for _, b in df_batch.iterrows():
            latex += " & \\textbf{"+b['code']+"} "
        latex += " & \\textbf{tot.} \\\\ \\hline \n"
        latex += "\\endhead \n"
        
        for i_r, s in df_shape_data.iterrows():
            if i_r % 2 == 1:
                latex += "\\rowcolor{lightgray} "
            
            latex += s['bakery_shape_code']
            q_tot = 0
            for _, b in df_batch.iterrows():
                if not math.isnan(s[b['id']]):
                    latex += " & "+str(int(s[b['id']]))
                    q_tot += s[b['id']]
                else:
                    latex += " & "
                
            latex += " & " + str(int(q_tot)) + "\\\\ \n"
                
                
        latex += """
        \\end{longtable}
        """
        return latex
    
    def _inner_latex_content_recipe(self):
        
        df_recipe, df_dough_sum, df_batch = self._get_recipe_data()
        
        df_product_data, df_product_batch = self._get_dough_by_product()
        
        df_batch.sort_values(by='position', 
                             ascending=False,
                             inplace=True)
        
        df_dough_sum.sort_values(by='bakery_dough_position',
                                 ascending=False,
                                 inplace=True)
        
        df_recipe.sort_values(by=['logistic_goods_position',
                                  'logistic_goods_name',
                                  'bakery_dough_as_recipe_position',
                                  'bakery_dough_old_sourdough',
                                  'bakery_dough_as_recipe_name'],
                                 ascending=[False, True, False, False, True],
                                 inplace=True)
        
        
        latex = "\\section*{Recettes}"
        
        for _, b in df_batch.iterrows():
            latex += "\\subsection*{"+b['name']+"}\n\n"
            
            for _, d in df_dough_sum.loc[df_dough_sum['bakery_batch_id']==b['id']].iterrows():
                if d['bakery_dough_sourdough']==1:
                    continue
                
                latex += """
                \\noindent\\vbox{
                \\noindent\\begin{tabular}{L{3cm}R{1.5cm}L{0.5cm}}
                """
                
                dough_name = ''
                if self.debug_mode:
                    dough_name += str(d['bakery_dough_id'])+" - "
                dough_name += d['bakery_dough_name']
                
                latex += "\\textbf{"+dough_name+"}"
                latex += " & \\textbf{"+str(weight_round(d['q']))+"}"
                latex += " & \\textbf{kg}\\\\ \\hline \n"
                
                for i_r, r in df_recipe.loc[(df_recipe['bakery_batch_id']==b['id'])\
                                          &(df_recipe['bakery_dough_id']==d['bakery_dough_id'])].reset_index().iterrows():
                    
                    name = ''
                    unit = ''
                    
                    if not math.isnan(r['logistic_goods_id']):
                        if self.debug_mode:
                            name += str(r['logistic_goods_id']) + ' - '
                        name += str(r['logistic_goods_name'])
                        unit = str(r['logistic_goods_unit'])
                            
                    elif not math.isnan(r['bakery_dough_as_recipe_id']):
                        if self.debug_mode:
                            name += str(r['bakery_dough_as_recipe_id'])+ ' - '
                        
                        if r['bakery_dough_as_recipe_sourdough']==1\
                            & d ['bakery_dough_old_sourdough']==1:
                            name += "``vieux'' "    
                        
                        name += str(r['bakery_dough_as_recipe_name'])
                        unit = 'kg'
                    
                    if i_r % 2 == 1:
                        latex += "\\rowcolor{lightgray} "
                    
                    latex += name + " & " + str(weight_round(r['q'])) + " & " + unit + "\\\\ \n"
                    
                latex += """
                \\end{tabular}
                
                \\medskip
                
                \\begin{flushright}
                \\footnotesize
                \\noindent \\textbf{Répartition}
                    
                \\noindent\\begin{tabular}{lR{1cm}l}
                """
                
                i_row=0
                for i_p, p in df_product_data.loc[df_product_data['bakery_dough_id_'+str(b['id'])]==d['bakery_dough_id']].reset_index().iterrows():
                    if not np.isnan(p['bakery_dough_q_'+str(b['id'])]):
                        if p['bakery_dough_q_'+str(b['id'])] > 0:
                            if i_row % 2 == 1:
                                latex += "\\rowcolor{lightgray} "
                            
                            latex += p['logistic_goods_code']
                            latex += ' & ' + str(weight_round(p['bakery_dough_q_'+str(b['id'])]))
                            latex += ' & kg \\\\ \n' 
                            i_row += 1
                
                latex += """
                \\end{tabular}
                \\end{flushright}
                }
                %\\bigskip
                """
        
        latex += "\\subsection*{Levains}"
        
        df_sourdough_sum = df_dough_sum.loc[df_dough_sum['bakery_dough_sourdough']==1, 
                                            ['bakery_dough_id', 
                                             'bakery_dough_name',
                                             'bakery_dough_position',
                                             'bakery_dough_king_sourdough_weight',
                                             'bakery_dough_old_sourdough',
                                             'q']].groupby(
                                                 ['bakery_dough_id', 
                                                  'bakery_dough_name',
                                                  'bakery_dough_position',
                                                  'bakery_dough_king_sourdough_weight',
                                                  'bakery_dough_old_sourdough']).sum().reset_index()
        
                                                 
                                                 
        for i_d, d in df_sourdough_sum.iterrows():
            # contrôle du vieux levain
            old_sourdough = df_recipe.loc[(df_recipe['bakery_dough_as_recipe_id']==d['bakery_dough_id'])\
                                            &(df_recipe['bakery_dough_old_sourdough']==1), 'q'].sum()
            
            if d['bakery_dough_king_sourdough_weight'] < old_sourdough:
                header_latex = "\\noindent\\textbf{\\color{red}Attention, le besoin en ``vieux'' " + d['bakery_dough_name']
                header_latex += " ("+str(weight_round(old_sourdough))+"~kg)"
                header_latex += " est supérieur au volume conservé "
                header_latex += " ("+str(weight_round(d['bakery_dough_king_sourdough_weight']))+"~kg).\\\\"
                header_latex += "Deux solutions à opérer dans l'onglet Recettes : \\begin{itemize}\n"
                header_latex += "\\item augmenter le volume de levain chef conservé.\n"
                header_latex += "\\item réduire le volume de vieux levain dans la recette.\n"
                header_latex += "\\end{itemize}}\n\n"
            
                latex = header_latex + latex 
            
            latex += """
            # \\noindent\\begin{tabular}{L{3cm}R{1.5cm}L{0.5cm}}
            # """
            
            latex += "\\textbf{"+d['bakery_dough_name']+"}"
            latex += " & \\textbf{"+str(weight_round(d['q']))+"}"
            latex += " & \\textbf{kg}\\\\ \\hline \n"
            
            df_sourdough_recipe = df_recipe.loc[df_recipe['bakery_dough_id']==d['bakery_dough_id'],
                                                ['logistic_goods_id',
                                                 'logistic_goods_name',
                                                 'logistic_goods_unit',
                                                 'bakery_dough_as_recipe_id',
                                                 'bakery_dough_as_recipe_sourdough',
                                                 'bakery_dough_as_recipe_name',
                                                 'q']].groupby(['logistic_goods_id',
                                                  'logistic_goods_name',
                                                  'logistic_goods_unit',
                                                  'bakery_dough_as_recipe_id',
                                                  'bakery_dough_as_recipe_sourdough',
                                                  'bakery_dough_as_recipe_name'],
                                                    dropna=False).sum().reset_index()
            
            for i_r, r in df_sourdough_recipe.iterrows():
                name = ''
                unit = ''
                
                if not math.isnan(r['logistic_goods_id']):
                    if self.debug_mode:
                        name += str(r['logistic_goods_id']) + ' - '
                    name += str(r['logistic_goods_name'])
                    unit = str(r['logistic_goods_unit'])
                        
                elif not math.isnan(r['bakery_dough_as_recipe_id']):
                    if self.debug_mode:
                        name += str(r['bakery_dough_as_recipe_id'])+ ' - '
                    
                    if r['bakery_dough_as_recipe_sourdough']==1\
                        & d ['bakery_dough_old_sourdough']==1:
                        name += "``vieux'' "    
                    
                    name += str(r['bakery_dough_as_recipe_name'])
                    unit = 'kg'
                
                if i_r % 2 == 1:
                    latex += "\\rowcolor{lightgray} "
                
                latex += name + " & " + str(weight_round(r['q'])) + " & " + unit + "\\\\ \n"
                
            refresh_rate = df_sourdough_recipe.loc[df_sourdough_recipe['bakery_dough_as_recipe_id']==d['bakery_dough_id'], 'q'].sum()\
                / df_sourdough_recipe['q'].sum() * 100  
            
            refresh_rate = '{:.2f}'.format(round(refresh_rate, 2))
            
            latex += """
            # \\end{tabular}
            {\\footnotesize
            \\noindent Taux de rafraîchi : """+refresh_rate+""" \\%\\\\
            Reste à conserver : """+str(weight_round(d['bakery_dough_king_sourdough_weight']))+""" kg.\\\\
            }
            
            # \\bigskip
            # """
                  
        
        return latex
    
    def _inner_latex_content_goods(self):
        
        df_goods_by_dough_sum, df_goods_sum = self._get_goods_data()
        
        df_goods_sum.sort_values(by=['logistic_goods_position',
                                     'logistic_goods_name',
                                     'bakery_dough_as_recipe_position',
                                     'bakery_dough_old_sourdough',
                                     'bakery_dough_as_recipe_name'],
                                 ascending=[False, True, False, False, True],
                                 inplace=True)
        
        df_goods_by_dough_sum.sort_values(by=['bakery_dough_position',
                                              'bakery_dough_name'],
                                          ascending=[False, True])
        
        latex = """
        \\section*{Pesées multiples}
        """
        
        for _, g in df_goods_sum.iterrows():
            if not math.isnan(g['logistic_goods_id']):
                selected_dough = df_goods_by_dough_sum.loc[(df_goods_by_dough_sum['logistic_goods_id']==g['logistic_goods_id'])]
                unit = g['logistic_goods_unit']
                
            elif not math.isnan(g['bakery_dough_as_recipe_id']):
                selected_dough = df_goods_by_dough_sum.loc[(df_goods_by_dough_sum['bakery_dough_as_recipe_id']==g['bakery_dough_as_recipe_id'])\
                                                           &(df_goods_by_dough_sum['bakery_dough_old_sourdough']==g['bakery_dough_old_sourdough'])]
                unit = 'kg'
            
            if len(selected_dough.index) == 1:
                continue
            
            selected_dough.reset_index(inplace=True)
            
            latex += """
            \\noindent\\begin{tabular}{L{3cm}R{1.5cm}L{0.5cm}}
            """
            
            name = ''
            if not math.isnan(g['logistic_goods_id']):
                name += str(g['logistic_goods_name'])
                unit = str(g['logistic_goods_unit'])
                
            elif not math.isnan(g['bakery_dough_as_recipe_id']):
                if g['bakery_dough_as_recipe_sourdough']==1\
                    and g ['bakery_dough_old_sourdough']==1:
                    name += "``vieux'' "    
                
                name += str(g['bakery_dough_as_recipe_name'])
                unit = 'kg'
                
            latex += "\\textbf{"+name+"}"
            latex += " & \\textbf{"+str(weight_round(g['q']))+"}"
            latex += " & \\textbf{"+unit+"}\\\\ \\hline \n"
            
            
            
            for i_r, d in selected_dough.iterrows():
                name = d['bakery_dough_name']
                
                if i_r % 2 == 1:
                    latex += "\\rowcolor{lightgray} "
                
                latex += name + " & " + str(weight_round(d['q'])) + " & " + unit + "\\\\ \n"
            
            latex += """
            \\end{tabular}
            
            \\bigskip
            """
        return latex 
    
    def _inner_latex_content(self):
        
        latex = """
        
        \\begin{multicols*}{4}
        """
        
        latex += self._inner_latex_content_product()
        
        latex += self._inner_latex_content_shape()
        
        latex += self._inner_latex_content_recipe()
        
        # latex += self._inner_latex_content_goods()
        
        latex += """
        
        \\end{multicols*}
        """
        
        return latex
    
def sort_dict(a, l):
    index_map = {v: i for i, v in enumerate(l)}
    return sorted(a.items(), key=lambda pair: index_map[pair[0]])

def weight_round(v):
    return '{:.3f}'.format(round(v, 2))
        
def str_cut(s, lenght, align='left'):
    if len(s) >= lenght:
        return s[:lenght]
    
    if align == 'left':
        s = s + ' '.join('' for i in range(lenght))
        return s[:lenght]
    if align == 'right':
        s = ' '.join('' for i in range(lenght)) + s
        return s[len(s)-lenght:]
