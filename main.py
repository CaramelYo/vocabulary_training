import logging
import sys
import os
import tkinter as tk
import json


# logging setting
logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(name)-12s %(levelname)-8s\n%(message)s',
                    datefmt = '%Y-%m-%d %H:%M',
                    handlers = [logging.FileHandler('main.log', 'w', 'utf-8'), ])

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.DEBUG)
console.setFormatter(logging.Formatter('%(message)s'))
logging.getLogger('').addHandler(console)

# data
data_dir = 'data'
voca_path = os.path.join(data_dir, 'vocabulary.json')

# setting
sentence_width = 50
meaning_num = 3

# global variable
voca_json = None


def create_label_textbox(win, label_text, row, width = 20, height = 2):
    label = tk.Label(win, text = label_text)
    label.grid(row = row, column = 0)
    textbox = tk.Text(win, width = width, height = height)
    textbox.grid(row = row, column = 1)
    textbox.delete(1.0, tk.END)

    return label, textbox

def create_meaning_ui(win, label_text, row):
    meaning_label, meaning_textbox = create_label_textbox(win, 'meaning_%d' % row, row, 20, 2)

    pos_value = tk.StringVar(win)
    pos_value.set('n')

    pos_option = tk.OptionMenu(win, pos_value, 'n', 'vi', 'vt', 'adj', 'adv')
    pos_option.grid(row = row, column = 2)

    # sentence_textbox = tk.Text(win, width = sentence_width, height = 2)
    # sentence_textbox.grid(row = row, column = 3)
    # sentence_textbox.delete(1.0, tk.END)

    # sentence_ch_textbox = tk.Text(win, width = sentence_width, height = 2)
    # sentence_ch_textbox.grid(row = row, column = 4)
    # sentence_ch_textbox.delete(1.0, tk.END)

    # return [meaning_label, meaning_textbox, pos_option, pos_value, sentence_textbox, sentence_ch_textbox]

    return [meaning_label, meaning_textbox, pos_option, pos_value]

def saving_click():
    global voca_json, meaning_num
    global voca_label, voca_textbox, meaning_ui_list

    voca = voca_textbox.get(1.0, tk.END).strip()
    logging.debug('vocabulary = %s' % voca)

    voca_info = {}
    voca_info['vocabulary'] = voca
    
    for i in range(meaning_num):
        meaning = meaning_ui_list[i][1].get(1.0, tk.END).strip()
        logging.debug('meaning = %s' % meaning)

        if meaning != '':
            meaning_info = {}
            meaning_info['meaning'] = meaning
            meaning_info['pos'] = meaning_ui_list[i][3].get().strip()
            # meaning_info['ex'] = meaning_ui_list[i][4].get(1.0, tk.END).strip()
            # meaning_info['ex_ch'] = meaning_ui_list[i][5].get(1.0, tk.END).strip()

            voca_info['meaning_%d' % i] = meaning_info

    if voca not in voca_json:
        voca_json[voca] = voca_info
    else:
        logging.info('merge the voca_info')
        
        ori_voca_info = voca_json[voca]
           
    with open(voca_path, 'w', encoding = 'utf-8') as f:
        json.dump(voca_json, f, sort_keys = True, ensure_ascii = False)
    
    # reset the interface
    voca_textbox.delete(1.0, tk.END)
    for i in range(meaning_num):
        meaning_ui_list[i][1].delete(1.0, tk.END)
        # meaning_ui_list[i][4].delete(1.0, tk.END)
        # meaning_ui_list[i][5].delete(1.0, tk.END)


if __name__ == '__main__':
    win = tk.Tk()
    win.geometry('600x400')
    win.title('vocabulary training')
    
    voca_label, voca_textbox = create_label_textbox(win, 'vocabulary', 0, 20, 1)

    meaning_ui_list = []

    for i in range(meaning_num):
        meaning_ui_list.append(create_meaning_ui(win, 'meaning_%d' % i, i + 1))
    
    saving_but = tk.Button(win, text = 'save the vocabulary', command = saving_click)
    saving_but.grid(row = meaning_num + 1, column = 5)

    if voca_json is None and os.path.exists(voca_path):
        with open(voca_path, 'r', encoding = 'utf-8') as f:
            voca_json = json.load(f)
    elif voca_json is None and not os.path.exists(voca_path):
        voca_json = {}
    else:
        logging.error('unexpected situation during initializing voca_json')
        exit()

    win.mainloop()