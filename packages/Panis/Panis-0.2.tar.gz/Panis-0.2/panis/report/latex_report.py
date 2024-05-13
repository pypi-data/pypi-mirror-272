# -*- coding: utf-8 -*-

import os, subprocess

from pathlib import Path
import tempfile

# TODO include lastpage package as ressource

class LatexReport():
    def __init__(self, 
                 farm, 
                 title='Rapport paille',
                 sector='LHF',
                 font_size=12,
                 geometry= """
                         a4paper,
                         inner=10 mm, 
                         outer=10 mm,
                         top=10 mm, 
                         headheight=-8pt,
                         bottom=10 mm,
                         landscape
                         """,
                 path_prefix = None,
                 clean=True):
        
        self.farm = farm
    
        self.font_size = font_size
        self.geometry = geometry
        
        self.title = title
        self.sector = sector
        
        self.path_prefix = path_prefix
        self.clean = clean
        
        if self.path_prefix is None:
            tmp_folder = tempfile.TemporaryDirectory('paille_tmp')
            self.farm.tmp_folders.append(tmp_folder)
            self.path_prefix = Path(tmp_folder.name) / 'report'
    
    def generate(self, open_file=False):
        self._generate_latex()
        self._generate_pdf(open_file=False)
        self._generate_pdf(open_file=open_file)
        
        if self.clean:
            self._clean()
        
    def _clean(self):
        ext = ['.tex', '.synctex.gz', '.aux', '.log']
        
        for e in ext:
            if os.path.isfile(self.path_prefix+e):
                os.system('rm '+self.path_prefix+e)
    
    def _generate_latex(self):
        self._clean()
        
        latex = self._header_latex_content()
        latex += self._inner_latex_content()
        latex += self._footer_latex_content()
        
        file_name = self.path_prefix + '.tex'
        
        f = open(file_name, 'a')
        f.write(latex)
        f.close()
    
    def _generate_pdf(self, open_file=False):
        os.system('lualatex -synctex=1 -interaction=nonstopmode '+self.path_prefix+'.tex')
        
        if open_file:
            subprocess.call(('xdg-open', self.path_prefix + '.pdf'))
        
        
    
    def _header_latex_content(self):
        colors = self.farm.logistic.goods.get_entries(columns=['color'], 
                                                      where="color <> ''")
        colors = [c[0] for c in colors]
        
        latex = """
        \\documentclass["""+str(self.font_size)+"""pt]{article}
        \\usepackage[utf8]{inputenc}
        \\usepackage[T1]{fontenc}
        \\usepackage{amsmath}
        \\usepackage{amssymb}
        \\usepackage{graphicx}
        \\usepackage[french]{babel}
        
        \\usepackage{multicol}
        %\\setlength{\\columnseprule}{1pt}
        
        \\usepackage{array}
        \\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}
        \\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}
        \\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}
                
        \\newcommand{\\toppagemargin}{17}
        \\newcommand{\\bottompagemargin}{10}
        
        \\usepackage{longtable}
        \\setlength{\LTpre}{0pt}
        \\setlength{\LTpost}{0pt}
        
        \\usepackage{colortbl}
        \\usepackage{seqsplit}
        
        \\usepackage{lastpage}
        	
        %\\usepackage{color, colortbl}
        \\usepackage[table]{xcolor}
        \\definecolor{lightgray}{gray}{0.85}
        \\definecolor{ffffff}{HTML}{ffffff}
        """
        
        for c in colors:
            latex += "\\definecolor{"+ c[1:] +"}{HTML}{"+ c[1:] +"}\n"
        
        latex +="""
        
        \\usepackage["""+self.geometry+"""]{geometry}
        
        \\usepackage{fancyhdr}
        
        \\usepackage[para]{footmisc}
        
        \\begin{document}
        \\pagestyle{fancy}
        \\renewcommand{\headrulewidth}{0pt}
        \\fancyhead{} % clear all header fields
        \\fancyhead[LO,LE]{\\textbf{"""+self.title+"""}}
        \\fancyhead[RE,RO]{\\thepage~/~\\pageref{LastPage}}
        \\fancyfoot{} % clear all footer fields
        %\\fancyfoot[LO,LE]{"""+self.sector+"""}
        
        
        """
        
        return latex
    
    def _inner_latex_content(self):
        return ""
    
    def _footer_latex_content(self):
        latex = """
        \\end{document}
        """
        return latex