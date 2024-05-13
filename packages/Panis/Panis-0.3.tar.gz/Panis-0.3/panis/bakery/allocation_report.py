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
        
        # retirer les products nuls
        df_product_data = df_product_data.loc[df_product_data[list(df_batch['bakery_batch_id'])].sum(axis=1)>0]
        
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
                
        
        # df_product_data columns 
        # 'bakery_product_id',
        # 'bakery_batch_id',
        # 'bakery_dough_id_'+str(b['id'])
        # 'bakery_dough_name_'+str(b['id']),
        # 'bakery_dough_baking_weight_loss_inverse_'+str(b['id']),
        # 'extra_dough_'+str(b['id'])
        # 'bakery_dough_q_'+str(b['id'])
        
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
        
        \\bigskip
        
        \\subsection*{Total boulange}
        
        \\noindent\\begin{longtable}[l]{@{}L{1cm}"""+'R{0.8cm}'.join(['' for i in range(df_batch.index.size+1)])+"""R{0.8cm}@{}}
        """
        
        q_by_batch = {}
        for _, b in df_batch.iterrows():
            q_by_batch[b['id']] = np.sum(df_product_data[b['id']] * df_product_data['bakery_product_weight'])
        
        latex += " "
        for _, b in df_batch.iterrows():
            latex += " &\\textbf{"+b['code']+"}"
        latex += "& \\textbf{tot.} \\\\ \\hline \n"
        latex += "\\endhead \n"
        
        latex += "en kg"
        for _, b in df_batch.iterrows():
            latex += " & " + str(int(np.round(q_by_batch[b['id']],0)))
        latex += " & " + str(int(np.round(np.sum(list(q_by_batch.values())),0)))
        
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
    
    def _get_dough_data(self):
        # le problème n'est pas simple à résoudre.
        # comme le temps de calcul n'est pas une contrainte,
        # appliquons une résolution simple comme si on le
        # faisait à la main.
        
        # on veut d'abord le poids des pâtes pour chaque batch
        # poids des levains compris.
        
        # pour ça, on part des produits commandés.
        # puis pour chaque pâte, on trouve la recette 
        # et on vérifie si il n'y a pas une pâte cachée dedans.
        
        # partons des produits commandés.
        df = self.farm.bakery.allocation.get_entries(
                columns = ['bakery_product_id', 'bakery_batch_id', 'quantity'],
                where='sales_distribution_id='+str(self.sales_distribution_id),
                pandas=True)
        df.columns = ['bakery_product_id', 'bakery_batch_id', 'bakery_allocation_quantity']
        
        # le résultat est en unité de pains. 
        # on a besoin du poids de l'unité de pain en kg.
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
        
        
        # df a donc comme colonnes :
        # 'bakery_product_id', 
        # 'bakery_batch_id', 
        # 'bakery_allocation_quantity',
        # 'logistic_goods_id',
        # 'bakery_product_weight',
        # 'bakery_shape_id'
        
        # chargeons les process et attribuons ainsi à chaque 
        # produit son dough associé
        df_process = self.farm.bakery.process.get_entries(columns=['bakery_product_id',
                                                                   'bakery_batch_id',
                                                                   'bakery_dough_id'],
                                                          pandas=True)
        df = df.merge(df_process,
                      on=['bakery_product_id', 
                          'bakery_batch_id'],
                      how='left')
        
        
        # df a donc comme colonnes :
        # 'bakery_product_id', 
        # 'bakery_batch_id', 
        # 'bakery_allocation_quantity',
        # 'logistic_goods_id',
        # 'bakery_product_weight',
        # 'bakery_shape_id',
        # 'bakery_dough_id'
        
        # chargeons les dough
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
        
        # et on peut calculer dès maintenant les quantités 
        # de dough
        df = df.merge(df_dough,
                      on='bakery_dough_id',
                      how='left')
        df['bakery_dough_quantity'] =\
                df['bakery_allocation_quantity']\
                * df['bakery_product_weight']\
                * df['bakery_dough_baking_weight_loss_inverse']\
                * (1 + df['bakery_dough_extra_dough'])
                
        # on vire l'occurence si la quantité est nulle
        df = df.loc[df['bakery_dough_quantity']>0]
        
        # df a donc comme colonnes :
        # 'bakery_product_id', 
        # 'bakery_batch_id', 
        # 'bakery_allocation_quantity',
        # 'logistic_goods_id',
        # 'bakery_product_weight',
        # 'bakery_shape_id',
        # 'bakery_dough_id',
        # 'bakery_dough_name',
        # 'bakery_dough_baking_weight_loss_inverse',
        # 'bakery_dough_sourdough',
        # 'bakery_dough_old_sourdough',
        # 'bakery_dough_king_sourdough_weight',
        # 'bakery_dough_extra_dough',
        # 'bakery_dough_position'
        # 'bakery_dough_quantity'
        
        # créons un dataframe contenant les dough nécessaires
        df_dough_needed = pd.DataFrame(columns=['bakery_dough_id', 
                                                'bakery_batch_id', 
                                                'quantity'])
        
        # chargeons les recettes des dough
        df_recipe = self.farm.bakery.recipe.get_entries(columns=['bakery_dough_id',
                                                                 'logistic_goods_id',
                                                                 'bakery_dough_as_recipe_id',
                                                                 'quantity'],
                                                        pandas=True)
        df_recipe.columns = ['bakery_dough_id',
                             'logistic_goods_id',
                             'bakery_dough_as_recipe_id',
                             'bakery_recipe_quantity']
        
        # on ajoute la quantité en pourcentage dans df_recipe
        df_recipe_sum = df_recipe[['bakery_dough_id', 'bakery_recipe_quantity']].groupby(['bakery_dough_id']).sum().reset_index()
        df_recipe_sum.columns = ['bakery_dough_id', 'bakery_recipe_quantity_sum']
        df_recipe = df_recipe.merge(df_recipe_sum,
                                    on='bakery_dough_id',
                                    how='left')
        
        df_recipe['bakery_recipe_quantity_percent'] = df_recipe['bakery_recipe_quantity'] / df_recipe['bakery_recipe_quantity_sum']
        
        # df_recipe a donc comme colonnes
        # 'bakery_dough_id',
        # 'logistic_goods_id',
        # 'bakery_dough_as_recipe_id',
        # 'bakery_recipe_quantity',
        # 'bakery_recipe_quantity_sum',
        # 'bakery_recipe_quantity_percent',
        
        # maintenant, on mouline a travers les produits 
        # pour déterminer les quantités de dough finales
        for _, d in df.iterrows():
            self._get_dough_data_recursive(df_recipe=df_recipe,
                                           bakery_dough_id=d['bakery_dough_id'],
                                           bakery_batch_id=d['bakery_batch_id'],
                                           bakery_dough_quantity=d['bakery_dough_quantity'],
                                           df_dough_needed=df_dough_needed)
        
        # il faut maintenant ajouter les levains chefs 
        # que l'on conservera d'ici la boulange suivante
        for _, d in df_dough.loc[df_dough['bakery_dough_sourdough']==1].iterrows():
            if d['bakery_dough_id'] in df_dough_needed['bakery_dough_id'].values:
                df_dough_needed.loc[len(df_dough_needed.index)] = \
                    [d['bakery_dough_id'],
                     df_dough_needed['bakery_batch_id'].min(),
                     d['bakery_dough_king_sourdough_weight']]
        
        # on agglomère les dough ensembles
        df_dough_needed = df_dough_needed.groupby(['bakery_dough_id',
                                                   'bakery_batch_id']).sum().reset_index()
        df_dough_needed.columns = ['bakery_dough_id',
                                 'bakery_batch_id',
                                 'bakery_dough_quantity']
        
        # on peut maintenant énumérer les recettes.
        # on exclue le levain qui est traité à part,
        # indépendamment des batch.
        # commençons par lui d'ailleurs.
        
        df_dough_needed = df_dough_needed.merge(df_dough[['bakery_dough_id',
                                                          'bakery_dough_sourdough']],
                                                on='bakery_dough_id',
                                                how='left')
        df_sourdough_needed = df_dough_needed.loc[df_dough_needed['bakery_dough_sourdough']==1]
        df_sourdough_needed = df_sourdough_needed[['bakery_dough_id', 
                                                    'bakery_dough_quantity']].groupby(['bakery_dough_id']).sum().reset_index()
        df_sourdough_needed.columns = ['bakery_dough_id',
                                       'bakery_dough_quantity']
        
        # on peut le retirer ensuite de df_dough_needed
        df_dough_needed = df_dough_needed.loc[df_dough_needed['bakery_dough_sourdough']==0]
        
        # on complète avec les infos des dough
        # et des ingrédients.
        # on commence par les dough
        df_dough_needed = df_dough_needed.merge(df_dough,
                                                on='bakery_dough_id',
                                                how='left')
        df_sourdough_needed = df_sourdough_needed.merge(df_dough,
                                                on='bakery_dough_id',
                                                how='left')
        
        # puis les ingrédients
        df_dough_needed = df_dough_needed.merge(df_recipe,
                                                on='bakery_dough_id',
                                                how='inner')
        df_sourdough_needed = df_sourdough_needed.merge(df_recipe,
                                                        on='bakery_dough_id',
                                                        how='inner')
        
        # on en profite pour calculer les quantités
        df_dough_needed['bakery_recipe_applied_quantity'] = df_dough_needed['bakery_dough_quantity'] * df_dough_needed['bakery_recipe_quantity_percent']
        df_sourdough_needed['bakery_recipe_applied_quantity'] = df_sourdough_needed['bakery_dough_quantity'] * df_sourdough_needed['bakery_recipe_quantity_percent']
        
        # et on vire la ligne si la quantité est nulle
        df_dough_needed = df_dough_needed.loc[df_dough_needed['bakery_recipe_applied_quantity']>0]
        df_sourdough_needed = df_sourdough_needed.loc[df_sourdough_needed['bakery_recipe_applied_quantity']>0]
                
        
        # puis logistic goods pour les ingrédients
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
        
        df_dough_needed = df_dough_needed.merge(df_goods,
                                                on='logistic_goods_id',
                                                how='left')
        df_sourdough_needed = df_sourdough_needed.merge(df_goods,
                                                        on='logistic_goods_id',
                                                        how='left')
        
        # puis dough pour les dough as recipe
        df_dough_as_recipe = df_dough[['bakery_dough_id', 
                                       'bakery_dough_name', 
                                       'bakery_dough_position']].copy()
        df_dough_as_recipe.columns = ['bakery_dough_as_recipe_id',
                                      'bakery_dough_as_recipe_name', 
                                      'bakery_dough_as_recipe_position']
        
        df_dough_needed = df_dough_needed.merge(df_dough_as_recipe,
                                                on='bakery_dough_as_recipe_id',
                                                how='left')
        df_sourdough_needed = df_sourdough_needed.merge(df_dough_as_recipe,
                                                        on='bakery_dough_as_recipe_id',
                                                        how='left')
        
        # enfin les batch 
        df_batch = self.farm.bakery.batch.get_entries(columns=['id',
                                                               'name',
                                                               'position'],
                                                        pandas=True)
        df_batch.columns = ['bakery_batch_id',
                            'bakery_batch_name',
                            'bakery_batch_position']
        df_dough_needed = df_dough_needed.merge(df_batch,
                                                on='bakery_batch_id',
                                                how='left')
        
        
        # on tri le tout
        df_dough_needed = df_dough_needed.sort_values(by=['bakery_batch_position', 
                                                          'bakery_dough_position',
                                                          'logistic_goods_position', 
                                                          'bakery_dough_as_recipe_position'],
                                                      ascending=[False, False, False, False]).reset_index()
        
        df_sourdough_needed = df_sourdough_needed.sort_values(by=['bakery_dough_position',
                                                                  'logistic_goods_position', 
                                                                  'bakery_dough_as_recipe_position'],
                                                              ascending=[False, False, False]).reset_index()
        
        
        return df_dough_needed, df_sourdough_needed
    
    
    def _get_dough_data_recursive(self, 
                                  df_recipe,
                                  bakery_dough_id,
                                  bakery_batch_id,
                                  bakery_dough_quantity,
                                  df_dough_needed):
        
        
        
        # on ajoute ce dough
        df_dough_needed.loc[len(df_dough_needed.index)] = \
            [bakery_dough_id,
             bakery_batch_id,
             bakery_dough_quantity]
        
        # on sélectionne les ingrédients de ce dough
        df_ingredients = df_recipe.loc[df_recipe['bakery_dough_id'] == bakery_dough_id]
        
        # on garde que les sous-dough
        df_ingredients = df_ingredients.loc[~ np.isnan(df_ingredients['bakery_dough_as_recipe_id'])]
        
        # on applique la récursivité 
        # en prenant soin de multiplier la quantité 
        # par le pourcentage indiqué par la recette
        for _, ingredient in df_ingredients.iterrows():
            self._get_dough_data_recursive(df_recipe=df_recipe,
                                           bakery_dough_id=ingredient['bakery_dough_as_recipe_id'], 
                                           bakery_batch_id=bakery_batch_id, 
                                           bakery_dough_quantity=bakery_dough_quantity * ingredient['bakery_recipe_quantity_percent'], 
                                           df_dough_needed=df_dough_needed)
        
    def _inner_latex_content_recipe(self):
        
        df_dough_needed, df_sourdough_needed = self._get_dough_data()
        
        latex = "\\section*{Levains}"  
        
        for i_d, d in df_sourdough_needed[['bakery_dough_id',
                                           'bakery_dough_name',
                                           'bakery_dough_quantity']].drop_duplicates().iterrows():
            
            latex += """
            \\noindent\\begin{tabular}{L{3cm}R{1.5cm}L{0.5cm}}
            """
            
            latex += "\\textbf{"+d['bakery_dough_name']+"}"
            latex += " & \\textbf{"+str(weight_round(d['bakery_dough_quantity']))+"}"
            latex += " & \\textbf{kg}\\\\ \\hline \n"
            
            df_focused_recipe = df_sourdough_needed.loc[df_sourdough_needed['bakery_dough_id']==d['bakery_dough_id']]
            
            for i_r, r in df_focused_recipe.iterrows():
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
                    
                    name += '\\emph{'+str(r['bakery_dough_as_recipe_name'])+'}'
                    unit = 'kg'
                
                if i_r % 2 == 1:
                    latex += "\\rowcolor{lightgray} "
                
                latex += name + " & " + str(weight_round(r['bakery_recipe_applied_quantity'])) + " & " + unit + "\\\\ \n"
                
            latex += """
            # \\end{tabular}
            # \\bigskip
            # """
        
        for i_b, b in df_dough_needed[['bakery_batch_id',
                                       'bakery_batch_name']].drop_duplicates().reset_index().iterrows():
            latex += """
            \\section*{"""+b['bakery_batch_name']+"""}
            """
            
            for i_d, d in df_dough_needed.loc[df_dough_needed['bakery_batch_id']==b['bakery_batch_id']][['bakery_dough_id',
                                                                                                         'bakery_batch_id',
                                                                                                         'bakery_dough_name',
                                                                                                         'bakery_dough_quantity']].drop_duplicates().reset_index().iterrows():
            
                latex += """
                \\noindent\\vbox{
                \\noindent\\begin{tabular}{L{3cm}R{1.5cm}L{0.5cm}}
                """
                
                dough_name = ''
                if self.debug_mode:
                    dough_name += str(d['bakery_dough_id'])+" - "
                dough_name += d['bakery_dough_name']
                
                latex += "\\textbf{"+dough_name+"}"
                latex += " & \\textbf{"+str(weight_round(d['bakery_dough_quantity']))+"}"
                latex += " & \\textbf{kg}\\\\ \\hline \n"
                
                df_focused_recipe = df_dough_needed.loc[(df_dough_needed['bakery_dough_id']==d['bakery_dough_id'])\
                                                        &(df_dough_needed['bakery_batch_id']==d['bakery_batch_id'])]
                
                for i_r, r in df_focused_recipe.iterrows():
                    
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
                        
                        name += '\\emph{'+str(r['bakery_dough_as_recipe_name'])+'}'
                        unit = 'kg'
                    
                    if i_r % 2 == 1:
                        latex += "\\rowcolor{lightgray} "
                    
                    latex += name + " & " + str(weight_round(r['bakery_recipe_applied_quantity'])) + " & " + unit + "\\\\ \n"
                    
                latex += """
                \\end{tabular}
                }
                
                \\bigskip
                """
        
            
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
