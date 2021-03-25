import re
import ezdxf
from pathlib import Path
from tkinter import *
from tkinter import filedialog

TASKS_PATH = Path(r'k:\Ficep_2')

def get_tasks():
    root = Tk()
    root.withdraw()
    root.filenames = filedialog.askopenfilenames(initialdir=TASKS_PATH,
                                               title="Select files",
                                               filetypes=(("ods files", "*.fnc"), ("all files", "*.*")))
    return root.filenames


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

        # if strr.isdecimal():
        #     return float(clean)
        # else:
        #     print('not decimal')
        #     return clean


def main(path):
    stem = path.stem
    name = Path(stem).with_suffix('.dxf')
    doc = ezdxf.new('R2000')
    msp = doc.modelspace()

    pts = []


    with open(path) as f:
        for line in f:
            if 'C:' in line:
                print(line, end='')
                continue
            if 'LP' in line:
                # print(line, end='')
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
                continue

            if all(i in line for i in('R', 'X', 'Y')):
                line = line.strip('[CUT] ')
                if 'SR1401' in line:
                    operation = 'CUT'


                if operation == 'VREZKA':
                    end_vrez = (get_data(line, 'X'), get_data(line, 'Y'))
                    msp.add_line(start_vrez, end_vrez, dxfattribs={'color': 11})
                    operation = ''

                elif operation == 'CUT':
                    pts.append((get_data(line, 'X'), get_data(line, 'Y')))
                    sr += 1

                print(pts)
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