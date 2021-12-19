# instance vai guardar a instância NK Landscape usada por PX e criada no main.py
import NKLandscape as nk
def init(_m, _k, _n):
    global n, k, m, instance
    n, k, m = _n, _k, _m
    instance = nk.NKLandscape(m, k, n)
