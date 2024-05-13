# -*- coding: utf-8 -*-

from ..table import timestamp_to_date
from ..report import LatexReport

import numpy as np
import pandas as pd

import math

class OrderReport(LatexReport):
    def __init__(self, 
                 farm, 
                 sales_distribution_id, 
                 debug_mode=False, 
                 **kwargs):
        self.sales_distribution_id = sales_distribution_id
        
        self.debug_mode=debug_mode
        
        self.distribution = farm.sales.distribution.get_entry(i=self.sales_distribution_id)
        self.distribution['human_date'] = timestamp_to_date(self.distribution['date'])
        
        LatexReport.__init__(self, 
                             farm, 
                             title = 'Distribution du '+self.distribution['human_date'],
                             sector='Fournil LHF',
                             font_size=10,
                             **kwargs)
    
    def _get_order_data(self):
        df_order = self.farm.sales.order.get_entries(columns=['id',
                                                              'sales_delivery_id',
                                                              'sales_client_id'],
                                                     where='sales_distribution_id='+str(self.sales_distribution_id))
        
        
        
    
    def _inner_latex_content(self):
        
        orders, deliveries, goods = self.farm.sales.product.get_orders_and_producs_by_distribution(sales_distribution_id=self.sales_distribution_id,
                                                                                                   sheet=False)
        goods.loc[goods['color'] == '', 'color'] = '#ffffff'  
        
        list_products = orders.columns.to_list()[7:-1]
        
        # security for not removed products
        for p in list_products:
            if p not in goods.index:
                del orders[p]
        
        list_products = orders.columns.to_list()[7:-1]
        
        # remove empty products
        for p in list_products:
            if orders[p].sum() == 0:
                del orders[p]
                list_products.remove(p)
        
        orders.loc[orders['sales_delivery_id'].isna(), 'sales_delivery_id'] = -1
        orders.loc[orders['sales_delivery_id']==-1, 'sales_delivery_name'] = "Livraison inconnue"
        # print(orders.loc[orders['sales_delivery_id']==-1])
        
        unique_deliveries = orders[['sales_delivery_id', 
                                    'sales_delivery_name']].drop_duplicates()
        
        unique_deliveries = unique_deliveries.merge(deliveries.reset_index(names='sales_delivery_id'),
                                                    how='left')
        unique_deliveries.sort_values(by='position',
                                      ascending=False,
                                      inplace=True)
        latex = ""
        
        if len(self.distribution['note'])>0:
            latex += '\\noindent '
            latex += self.distribution['note']
            latex += "\n\n"
        
        for i_d, d in unique_deliveries.reset_index().iterrows():
            if d['sales_delivery_id'] > 0:
                if deliveries.loc[d['sales_delivery_id'], 'new_page']==1:
                    latex += '\\newpage\n'
                    # latex += '~\\vspace{-1cm}\n\n'
                # elif i_d == 0:
                    # latex += '~\\vspace{-1cm}\n\n'
                else:
                    latex += '\\vspace{0.3cm}\n\n'
                
            if d['sales_delivery_name']=="Livraison inconnue":
                latex += '\\newpage\n'
                
            # latex += '\\section*{'+str(d['sales_delivery_name'])+'}\n'
            latex += '\n\n\\noindent\\begin{center}\\textbf{\\Large '+str(d['sales_delivery_name'])+'}\\end{center}\n\n'
            # latex += '\\vspace{0.3cm}\n\n'
            
            latex += "\n\\noindent\\begin{longtable}[l]{|L{2cm}"
            
            if d['market_sheet'] or d['unsold_line']:
                latex += "|L{1.5cm}"
            
            
            latex += "|"+"|".join([">{\\columncolor{"+goods.loc[p, 'color'][1:]+"}}R{0.7cm}" for i, p in enumerate(list_products)])+"|}"
            latex += "\n\\hline"
            
            latex += " & "
            
            if d['market_sheet']:
                latex += "suite ? & "
            
            if d['unsold_line']:
                latex += " & "
            
            latex += " & ".join(["\\textbf{\\scriptsize \\seqsplit{"+goods.loc[p,'code'] + "}}" for p in list_products])
            latex += "\\\\\n"
            latex += "\\hline\n"
            latex += "\\endhead\n"
            
            if orders.loc[orders['sales_delivery_id']==d['sales_delivery_id']].index.size > 1:
                s = orders.loc[orders['sales_delivery_id']==d['sales_delivery_id']].sum()
                latex += "\\rowcolor{lightgray}\\textbf{total} & "
                if d['market_sheet'] or d['unsold_line']:
                    latex += " & "
                latex += " & ".join(['{\\small '+string_quantity(s[p])+'}' for p in list_products])
                latex += "\\\\\n"
                latex += "\\hline\n"
            
            for _, o in orders.loc[orders['sales_delivery_id']==d['sales_delivery_id']].iterrows():
                latex += '{\\small '+o['sales_client_name'][:11]
                if len(o['sales_client_note']) > 0:
                    latex += '\\footnote{'+o['sales_client_note']+'}'
                latex += "} & "
                if d['market_sheet'] or d['unsold_line']:
                    latex += " & "
                latex += " & ".join(['{\\small '+string_quantity(o[p])+'}' for p in list_products])
                latex += "\\\\\n"
                latex += "\\hline\n"
            
            if d['unsold_line']:
                latex += "\\textbf{retours} & "
                if d['market_sheet'] or d['unsold_line']:
                    latex += " & "
                latex += " & ".join([' ' for p in list_products])
                latex += "\\\\\n"
                latex += "\\hline\n"
            
            latex += "\\end{longtable}\n"
            
            if len(d['note'])>0:
                latex += '\\noindent '
                latex += d['note']
                latex += "\n\n"
            
            if d['market_sheet']:
                latex += """
                
                \\bigskip
                
                \\noindent\\begin{minipage}[t]{0.8\\textwidth}
                \\textbf{Notes :}
                \\end{minipage}
                \\begin{minipage}[t]{0.2\\textwidth}
                \\textbf{Retours des livraisons :}
                \\end{minipage}
                \\vfill
                \\hfill\\begin{minipage}[t]{0.2\\textwidth}
                \\textbf{Farine 1kg :}\\\\
                \\textbf{Farine 3kg :}
                \\vspace{0.5cm}
                \\end{minipage}
                """
        
        return latex

def string_quantity(q):
    if q > 0:
        return str(q)
    else:
        return ''