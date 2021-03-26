import re
import ezdxf
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from ezdxf.math import Vec2
from math import sqrt

TASKS_PATH = Path(r'k:\Ficep_2')

def get_tasks():
    root = Tk()
    root.withdraw()
    root.filenames = filedialog.askopenfilenames(initialdir=TASKS_PATH,
                                               title="Select files",
                                               filetypes=(("ods files", "*.fnc"), ("all files", "*.*")))
    return root.filenames


def bulge_from_rad(pt1, pt2, rad):
    dist = (Vec2(pt1) - Vec2(pt2)).magnitude
    bulge = (2*(rad-sqrt(abs((dist*dist)/4 - rad*rad))))/dist
    return bulge


def get_data(str, sym=''):
    res = re.search(f'{sym}\S+', str)
    if res:
        strr = res.group(0)
        # print(strr)
        clean = strr.strip(sym)
        # print(clean)
        try:
            N = float(clean)
            return N
        except (ValueError, TypeError):
            return clean


def get_new_pt(line, pts, rad=0):
    pt2 = (get_data(line, 'X'), get_data(line, 'Y'))
    if rad:
        return (get_data(line, 'X'), get_data(line, 'Y'), bulge_from_rad(pts[-1], pt2, rad))
    else:
        return (get_data(line, 'X'), get_data(line, 'Y'))



def main(path):
    stem = path.stem
    name = Path(stem).with_suffix('.dxf')
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()

    pts = []
    switch = 1
    operation = ''  # VREZKA, CUT, VYHOD

    with open(path) as f:
        for line in f:

            if 'LP' in line:

                B = get_data(line, 'SA')
                L = get_data(line, 'LP')

                msp.add_lwpolyline(((0, 0),(0, B),(L, B),(L, 0)), close=True)

                continue

            if 'ANG' in line:
                line = line.strip('[MARK] ')

                msp.add_text(get_data(line, 'N:'),  dxfattribs={'height': 10,
                                                                'rotation': get_data(line, 'ANG'),
                                                                'color': 140

                                                                }).set_pos(
                    [get_data(line, 'X'),
                     get_data(line, 'Y')],
                    align='TOP_LEFT')

                print('MARK: ', line, end='')
                continue

            if 'TS33' in line:
                line = line.strip('[HOL] ')
                print('HOLE: ', line, end='')

                msp.add_circle(
                    [get_data(line, 'X'), get_data(line, 'Y')],
                    get_data(line, 'DC') / 2
                )

                continue

            if 'LEAD' in line:
                line = line.strip('[LEAD] ')
                start_vrez = (get_data(line, 'X'), get_data(line, 'Y'))
                operation = 'VREZKA'
                switch += 1
                continue

            if 'SR1401' in line:
                switch = 3333

            if all(i in line for i in('R', 'X', 'Y')):
                line = line.strip('[CUT] ')
                switch += 1
                # if 'SR1401' in line:
                #     sr = 1

                if operation == 'VREZKA':
                    end_vrez = (get_data(line, 'X'), get_data(line, 'Y'), get_data(line, 'R'))
                    msp.add_line(start_vrez, end_vrez, dxfattribs={'color': 11})
                    pts.append(end_vrez)
                    operation = 'CUT'

                if operation == 'CUT' and switch <= 3334:
                    # pts.append((get_data(line, 'X'), get_data(line, 'Y'), get_data(line, 'R')))
                    pts.append(get_new_pt(line, pts, get_data(line, 'R')))
                elif operation == 'CUT' and switch > 3334:
                    start_vyhod = (get_data(line, 'X'), get_data(line, 'Y'), get_data(line, 'R'))
                    pts.append(start_vyhod)
                    msp.add_lwpolyline(pts, format='xyb')
                    pts = []
                    operation = 'VYHOD'

                if operation == 'VYHOD':
                    end_vyhod = (get_data(line, 'X'), get_data(line, 'Y'))
                    # end_vyhod = get_new_pt(line, pts, get_data(line, 'R'))
                    msp.add_line(start_vyhod, end_vyhod, dxfattribs={'color': 140})
                    switch = 1
                # elif operation == 'CUT' and sr != 2:
                #     pts.append((get_data(line, 'X'), get_data(line, 'Y')))
                #     sr += 1

                # print(pts)
                continue
    # msp.add_line([0,0], [500,500])
    # msp.add_circle([0,0], 50)
    # msp.add_text([50,0],'DSFSDFSD')
    doc.saveas(name)


if __name__ == '__main__':
    # str = 'TS33 DC28 X670.94 Y750.11'
    # print(get_data(str, sym='DC'))
    files = get_tasks()
    for file in files:
        main(Path(file))