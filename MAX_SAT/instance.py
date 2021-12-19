# instance vai guardar a instância NK Landscape usada por PX e criada no main.py
import MAXSAT as ms
def init(inst_file):
    global instance
    instance = ms.MAXSAT(inst_file)
