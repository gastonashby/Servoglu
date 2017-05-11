
import ParsingMathML as mp
from DefineFunction import *

import numpy as np

from scipy.integrate import odeint
import EdfWriter as edf

def RunTest(FileName):
    _u,_c,_f,_e = mp.ParseMathml('Glucosafe.xml','LanguageSupport.csv')
    _aux = []
    exec(defineUserDefinedParameters(_u), globals())
    exec(defineParameters(_c), globals())
    exec(defineFunctions(_f),globals())
    exec(defineEquations(_e),globals())
    _xdata = np.linspace(0, 1000, 1000)
    _y = odeint(fGluc, _aux, _xdata)
    edf.WriteEDF(_y, _e, 1 / 60, FileName)

    indexGr = 1

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


