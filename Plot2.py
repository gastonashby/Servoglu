
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


def recalculate(indexGr):
    global _y, _aux, _xdata
    print(indexGr)
    #print(_y[indx-1])
    _aux = _y[indexGr-1]
    _xdata = np.linspace(indexGr-1, indexGr + 9999, 10000)
    print(_y)

    _y = odeint(fGluc, _aux, _xdata)
    print(_y)


def fGluc(XX, tt):
    global _e

    _i = 0
    salida = []
    for ec in _e:
        print(eval('XX[' + str(_i) + ']'))
        auux = ec.name + '= XX[' + str(_i) + ']'
        _i += 1
        exec(auux)
    print('********')
    for eq in _e:
       # print(eq.equation)
        salida.append(eval(eq.equation))

    return salida

_xdata = np.linspace(0, 10000, 10000)
_y = odeint(fGluc, _aux, _xdata)

#print(_y)
#edf.WriteEDF(_y,_e,1/60,'sampleEDF')

#print(y)



def obtener(_i):
    global _y
    return _y[_i]

