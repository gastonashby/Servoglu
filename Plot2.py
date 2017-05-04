
import ParsingMathML as mp
from DefineFunction import *

import numpy as np

from scipy.integrate import odeint

_u,_c,_f,_e = mp.ParseMathml('Glucosafe.xml','LanguageSupport.csv')
_aux = []
exec(defineUserDefinedParameters(_u), globals())
exec(defineParameters(_c), globals())
exec(defineFunctions(_f),globals())
exec(defineEquations(_e),globals())


def recalculate(indx):
    global _y, _aux, _xdata
    #print(_aux)
    #print(_y[indx-1])
    _aux = _y[indx-1]
    _y = odeint(fGluc, _aux, _xdata)


def fGluc(XX, tt):
    global _e

    _i = 0
    salida = []
    for ec in _e:
        auux = ec.name + '= XX[' + str(_i) + ']'
        _i += 1
        #print(auux)
        exec(auux)

    for eq in _e:
       # print(eq.equation)
        salida.append(eval(eq.equation))

    return salida

_xdata = np.linspace(0, 10000, 10000)
_y = odeint(fGluc, _aux, _xdata)
#print(y)

def obtener(_i):
    global _y
    return _y[_i]

