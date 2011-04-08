#!/usr/bin/env python
import string
from pprint import pprint

header = '''
\\begin{tikzpicture}
\\draw[gray] (0,0) grid [step=1] (9,9);
\\draw[thick] (0,0) grid [step=3] (9,9);
'''
trail = '\\end{tikzpicture}'
cell = '\\node at (%(x).1f,%(y).1f) {\\Large{%(c)s}};'
cell_solution = '\\node at (%(x).1f,%(y).1f) {\\Large{\\textcolor{red}{%(c)s}}};'

N = 9 # For the moment, we fix the dimension to 9x9

def parse_sudoku(p, sep):
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

def save_tikz(p, file_name, sep=' '):
    d = parse_sudoku(p, sep)
    tikz_lines = get_tikz_lines(d)
    s = header + '\n'.join(tikz_lines) + '\n' + trail + '\n'
    f = open(file_name, 'w')
    f.write(s)
    f.close()
    
p1 = '''
9 . . 4 . . . 1 6
2 . . . 5 6 7 . .
. . . 8 7 1 4 . 2
6 3 . . 1 . . 5 .
. . . . 8 . . . . 
. 7 . . 3 . . 4 9 
7 . 6 2 4 8 . . .
. . 8 3 9 . . . 4 
3 9 . . . 7 . . 5
'''

p2 = '''
|5|3| | |7| | | | |.
|6| | |1|9|5| | | |.
| |9|8| | | | |6| |.
|8| | | |6| | | |3|.
|4| | |8| |3| | |1|.
|7| | | |2| | | |6|.
| |6| | | | |2|8| |.
| | | |4|1|9| | |5|.
| | | | |8| | |7|9|.'''

p2s = '''
|5|3|4s|6s|7|8s|9s|1s|2s|.
|6|7s|2s|1|9|5|3s|4s|8s|.
|1s|9|8|3s|4s|2s|5s|6|7s|.
|8|5s|9s|7s|6|1s|4s|2s|3|.
|4|2s|6s|8|5s|3|7s|9s|1|.
|7|1s|3s|9s|2|4s|8s|5s|6|.
|9s|6|1s|5s|3s|7s|2|8|4s|.
|2s|8s|7s|4|1|9|6s|3s|5|.
|3s|4s|5s|2s|8|6s|1s|7|9|.'''

if __name__ == '__main__':
    save_tikz(p2, 'sudoku2.tikz', '|')
    save_tikz(p2s, 'sudoku2s.tikz', '|')
