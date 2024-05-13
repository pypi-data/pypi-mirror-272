# -*- coding: utf-8 -*-

import paille

path = '/home/fremi/Documents/Agriculture/LHF/Boulangerie/nextcloud/lhf.db'

#%%
lhf = paille.Farm(path)

#%%
paille.gui.start(path)

#%%
# lhf._commit("""
#             ALTER TABLE sales_product
# ADD new_quantity REAL DEFAULT 0.0; 
#             """)
            
# product = lhf.sales.product.get_entries(columns=['id', 'quantity'], list_dict=True)
# for p in product:
#     lhf.sales.product.update_entry(i=p['id'],
#                                    new_quantity=p['quantity'])

# lhf._commit("""
#             ALTER TABLE sales_product
#             DROP COLUMN quantity
#             """)

# lhf._commit("""
#             ALTER TABLE sales_product
#             RENAME COLUMN new_quantity TO quantity
#             """)

#%%
# print(lhf.bakery.allocation.get_dough_quantity(sales_distribution_id=5, 
                                         # bakery_batch_id=7))

# print(lhf.bakery.allocation.get_dough_quantity(sales_distribution_id=5, 
                                         # bakery_batch_id=8))

#%%
lhf.sales.order.report(sales_distribution_id=7,
                       open_file=True,
                       path_prefix='order_report',
                       debug_mode=False,
                       clean=True)

#%%
lhf.bakery.allocation.report(sales_distribution_id=8, 
                             open_file=True, 
                             path_prefix='alloc_report',
                             debug_mode=False,
                             clean=True)

# ajouter un warning si levain insuffisant.

#%%
br = paille.bakery.allocation_report.BakingReport(farm=lhf, 
                                                 sales_distribution_id=1)
# df_recipe, df_dough_sum, df_batch = br._get_recipe_data()
df_product_data, df_batch = br._get_dough_by_product()
# df_goods_by_dough_sum, df_goods_sum = br._get_goods_data()

# TO2000 id 36, product id 15
# avec TO 42.27 SCF1, VA 11.58, levain 1.91 / 7.96
# sans TO 24.2 SCF1, VA 6.63, levain 1.18 / 7.23

# recette 2.1 SCF1, 0.15 graines
# on ajoute à sans 8 TO2000 soit 16kg cuit
# ça correspond à 19.36kg cru
# ça correspond à 0.93*19.36=18.069 de SCF1
# ça nous ramène bien à 42.27 SCF1
# pour la VA, l'ajout de 18.069kg de SCF1 correspond à 4.93
# on retrouve bien le VA avec TO.

# en ajoutant le TO, on ajoute 18.069 de SCF1
# soit 0.048*18.069=0.881 de levain


#%%
# lhf.logistic.goods.insert_entry(name='beurre Pré Joly', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='chocolat en poudre', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='chocolat pépites', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='eau', unit='l', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name="eau fleur d'oranger", unit='l', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='farine blé VA', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='farine blé VM', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='farine PE', unit='kg', trigger_bakery=True, trigger_mill=True)
# lhf.logistic.goods.insert_entry(name='figues morceaux', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='graines courge', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='graines lin', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='graines pavot', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='graines sésame', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='graines tournesol', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='lait', unit='l', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='levain', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='noisettes', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='œufs', unit='unité', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='sel gros', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='son', unit='kg', trigger_bakery=True)
# lhf.logistic.goods.insert_entry(name='sucre complet', unit='kg', trigger_bakery=True)

# lhf.bakery.product.create(name='Semi-Complet Petit Moulé', code='SCPM')
# lhf.bakery.product.create(name='Semi-Complet Grand Moulé', code='SCGM')
# lhf.bakery.product.create(name='FNPM', code='FNPM')
# lhf.bakery.product.create(name='FNGM', code='FNGM')
# lhf.bakery.product.create(name='SC1000', code='SC1000')
# lhf.bakery.product.create(name='SC1500', code='SC1500')
# lhf.bakery.product.create(name='T110GM', code='T110GM')
# lhf.bakery.product.create(name='T110PM', code='T110PM')
# lhf.bakery.product.create(name='COPM', code='COPM')
# lhf.bakery.product.create(name='COGM', code='COGM')
# lhf.bakery.product.create(name='GRGM', code='GRPM')
# lhf.bakery.product.create(name='SE800', code='SE800')
# lhf.bakery.product.create(name='BR800', code='BR800')
# lhf.bakery.product.create(name='BR300', code='BR300')
# lhf.bakery.product.create(name='TO2000', code='TO2000')

# #%%
# lhf.bakery.dough.insert_entry(name='SC F1', baking_weight_loss_inverse=1.21, position=1)
# lhf.bakery.dough.insert_entry(name='PE F1', baking_weight_loss_inverse=1.21),
# lhf.bakery.dough.insert_entry(name='FINOI F1', baking_weight_loss_inverse=1.21),
# lhf.bakery.dough.insert_entry(name='T110 F1', baking_weight_loss_inverse=1.21),
# lhf.bakery.dough.insert_entry(name='SC F2', baking_weight_loss_inverse=1.21),
# lhf.bakery.dough.insert_entry(name='Extra graines TO', baking_weight_loss_inverse=1),
# lhf.bakery.dough.insert_entry(name='Graine F2', baking_weight_loss_inverse=1.21),
# lhf.bakery.dough.insert_entry(name='Seigle F1', baking_weight_loss_inverse=1.21),
# lhf.bakery.dough.insert_entry(name='Courge F2', baking_weight_loss_inverse=1.21),
# lhf.bakery.dough.insert_entry(name='BR F1', baking_weight_loss_inverse=1.21),
# lhf.bakery.dough.insert_entry(name='Extra pépites ESC', baking_weight_loss_inverse=1),
# lhf.bakery.dough.insert_entry(name='Extra Cacao Choco', baking_weight_loss_inverse=1);

# #%%
# lhf.bakery.shape.insert_entry(name='Grand Moulé',
#                               code='GM',
#                               position=5)
# lhf.bakery.shape.insert_entry(name='Petit Moulé',
#                               code='PM',
#                               position=4)
# lhf.bakery.shape.insert_entry(name='Grand Banneton',
#                               code='GB',
#                               position=3)
# lhf.bakery.shape.insert_entry(name='Moyen Banneton',
#                               code='MB',
#                               position=2)
# lhf.bakery.shape.insert_entry(name='Petit Banneton',
#                               code='PB',
#                               position=1)

# #%%
# lhf.bakery.batch.insert_entry(name='Cuisson 1',
#                               code='F1',
#                               position=5)
# lhf.bakery.batch.insert_entry(name='Cuisson 2',
#                               code='F2',
#                               position=4)
# lhf.bakery.batch.insert_entry(name='Cuisson 3',
#                               code='F3',
#                               position=3)

# #%%
# lhf.bakery.recipe.insert_entry(
#                  bakery_dough_id=2,
#                  logistic_goods_id=5,
#                  quantity=3.2)
# lhf.bakery.recipe.insert_entry(
#                  bakery_dough_id=2,
#                  logistic_goods_id=8,
#                  quantity=49.3)

# #%%
# lhf.sales.distribution.insert_entry_as_human(date='26/01/2024')
# lhf.sales.distribution.insert_entry_as_human(date='23/01/2024')
# lhf.sales.distribution.insert_entry_as_human(date='29/01/2024')

# #%%
# lhf.sales.delivery.insert_entry(name='Pré Joly')
# lhf.sales.delivery.insert_entry(name='Croix Blanche')
# lhf.sales.delivery.insert_entry(name='Marché Les Halles')
# lhf.sales.delivery.insert_entry(name='Marché Châteauneuf')

# #%%
# lhf.sales.client.insert_entry(name='Marché Les Halles')
# lhf.sales.client.insert_entry(name='Marché Châteauneuf')
# lhf.sales.client.insert_entry(name='Roux', first_name='Gilbert')

# #%%
# lhf.sales.order.insert_entry(sales_distribution_id=1,
#                              sales_delivery_id=3,
#                              sales_client_id=3)
# lhf.sales.order.insert_entry(sales_distribution_id=1,
#                              sales_delivery_id=3,
#                              sales_client_id=1)

# #%%
# lhf.sales.order.count_by_sales_distribution()

# #%%
# lhf.sales.order.count_by_sales_delivery(sales_distribution_id=1)