#!/usr/bin/env python
import os.path
import tempfile
import shutil
from optparse import OptionParser
from subprocess import call
from pprint import pprint

header = r'''\begin{tikzpicture}
\draw[gray] (0,0) grid [step=1] (9,9);
\draw[thick] (0,0) grid [step=3] (9,9);
'''
footnote = r'\node[anchor=north west] at (0,0) {\tiny{\textsf{Start position in black, solution in red}}};'
trail = r'''\end{tikzpicture}'''
cell = r'\node at (%(x).1f,%(y).1f) {\Large{%(c)s}};'
cell_solution = r'\node at (%(x).1f,%(y).1f) {\Large{\textcolor{red}{%(c)s}}};'

N = 9 # For the moment, we fix the dimension to 9x9

latex_header = r'''
\documentclass{article}
\usepackage{tikz,amsmath,siunitx}
\usetikzlibrary{arrows,snakes,backgrounds,patterns,matrix,shapes,fit,calc,shadows,plotmarks}
\usepackage[graphics,tightpage,active]{preview}
\PreviewEnvironment{tikzpicture}
\PreviewEnvironment{equation}
\PreviewEnvironment{equation*}
\newlength{\imagewidth}
\newlength{\imagescale}
\pagestyle{empty}
\thispagestyle{empty}
\begin{document}'''

latex_trail = r'''
\end{document}
'''


def parse_sudoku(p):
    if p.count('|'):
        sep = '|'
    else:
        sep = ' '
    d = [[e for e in line.split(sep) if len(e)>0] for line in p.split('\n')]
    d = [r for r in d if len(r)>0]
    d.reverse()
    return d

def get_tikz_lines(d):
    lines = []
    for j, row in enumerate(d):
        for i, c in enumerate(row):
            x = i + 0.5
            y = j + 0.5
            if c.isdigit():
                lines.append(cell % locals())
            elif c.count('s'):
                c = c[0]
                lines.append(cell_solution % locals())
            
    return lines

def get_tikz(d, options):
    tikz_lines = get_tikz_lines(d)
    if options.footnote:
        ft = footnote
    else:
        ft = ''
    parts = [header, '\n'.join(tikz_lines), ft, trail]
    s = '\n'.join(parts) + '\n'
    return s
    
def make_pdf(tikz, file_name):
    latex = latex_header + tikz + latex_trail
    tmp_dir = tempfile.mkdtemp()
    base_latex_file = os.path.join(tmp_dir, file_name)
    latex_file = base_latex_file + '.tex'
    f = open(latex_file, 'w')
    f.write(latex)
    f.close()
    call(('pdflatex', latex_file), cwd=tmp_dir)
    shutil.copyfile(base_latex_file + '.pdf', file_name + '.pdf')
    shutil.rmtree(tmp_dir)
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-t', action='store_false', dest='out_tikz',
                      default=True, help='Output tikz file')
    parser.add_option('-p', action='store_true', dest='out_pdf',
                      default=False, help='Output PDF file')
    parser.add_option('-f', action='store_true', dest='footnote',
                      default=False, help='Add footnote')
    (options, args) = parser.parse_args()
    
    for file_name in args:
        try:
            f = open(file_name, 'r')
        except IOError:
            print "The file", f, "doesn't exist."
        else:
            p = f.read()
            d = parse_sudoku(p)
            f.close()
            base_name = os.path.splitext(file_name)[0]
            tikz = get_tikz(d, options)
            if options.out_tikz:
                f = open(base_name + '.tikz', 'w')
                f.write(tikz)
                f.close()
            if options.out_pdf:
                make_pdf(tikz, base_name)
