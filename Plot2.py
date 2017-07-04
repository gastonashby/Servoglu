
#import ParsingMathML as mp
from DefineFunction import *

import numpy as np
import ModelParser as mp

from scipy.integrate import odeint
import EdfWriter as edf

model = mp.ModelParser('Glucosafe.xml','LanguageSupport.csv')
_u = model.userDefinedParameters
_c = model.constants
_f = model.functions
_e = model.equations


_aux = []
exec(defineUserDefinedParameters(_u), globals())
exec(defineParameters(_c), globals())
exec(defineFunctions(_f),globals())
exec(defineEquations(_e),globals())

indexGrAux = 0


def recalculate1():
    global indexGrAux
    print('5')
    recalculate(indexGrAux)


def recalculate(indexGr):
    global _y, _aux, _xdata, indexGrAux
    _aux = _y[indexGr]
    print('4')
    _xdata = np.linspace(indexGr, indexGr + 999, 1000)
    indexGrAux = 0
    _y = odeint(fGluc, _aux, _xdata)
    print(_y)


def fGluc(XX, tt):
    global _e
    _i = 0
    salida = []
    for ec in _e:
        #print(eval('XX[' + str(_i) + ']'))
        auux = ec.name + '= XX[' + str(_i) + ']'
        _i += 1
        exec(auux)
    #print('********')
    for eq in _e:
       # print(eq.equation)
        salida.append(eval(eq.equation))

    return salida


_auxIni = _aux
_xdata = np.linspace(0, 999, 1000)
_y = odeint(fGluc, _aux, _xdata)
print('Solution created 1st time')

def restart():
    global  _y, _auxIni
    _xdata = np.linspace(0, 999, 1000)
    _y = odeint(fGluc, _auxIni, _xdata)


def obtener(_i):
    global _y
    print('2')
    print(_i)
    print(_y)
    return _y[_i]

