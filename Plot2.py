
#import ParsingMathML as mp
from DefineFunction import *

import numpy as np
import ModelParser as mp

from scipy.integrate import odeint


model = mp.ModelParser('Glucosafe.xml', 'LanguageSupport.csv')
_u = model.userDefinedParameters
_c = model.constants
_f = model.functions
_e = model.equations

def updateCalculatedConstants():
    for _i in range(0, len(_calculated)-1):
        #print(eval(_calculated[_i]))
        #print(_calculated[_i])
        exec(_calculated[_i], globals())
    #print(eval("ABSA"))

def updateFunctions():
    for _i in range(0, len(_functionList)-1):
        #print(eval(_functionList[_i] + _paramsList[_i]))
        #print(_functionList[_i] + _paramsList[_i])
        eval(_functionList[_i] + _paramsList[_i])

_aux = []
exec(defineUserDefinedParameters(_u), globals())
_constants, _calculated = defineParameters(_c)
exec(_constants, globals())
_functionList, _paramsList = defineFunctionList(_f)
exec(defineFunctions(_f),globals())
exec(defineEquations(_e),globals())

indexGrAux = 0

_auxIni = _aux
_xdata = np.linspace(0, 999, 1000)


def odesys(XX, tt):
    global _e
    _i = 0
    salida = []
    for ec in _e:
        #print(eval('XX[' + str(_i) + ']'))
        auux = ec.name + '= XX[' + str(_i) + ']'
        _i += 1
        exec(auux)

    for eq in _e:
        salida.append(eval(eq.equation))

    return salida

#print(_xdata)
_sol = odeint(odesys, _aux, _xdata)
print('Solution created 1st time')


def change_scale(step):
    global _xdata
    _xdata = np.linspace(0, 999 * step, 1000)

def recalculate():
    global _sol, _aux, _xdata, indexGrAux, _c
    _aux = _sol[indexGrAux-1]
    indexGrAux = 1
    updateCalculatedConstants()
    updateFunctions()

    print(_sol)
    print("-- Recalculate --")
    _sol = odeint(odesys, _aux, _xdata)
    print(_sol)


def restart():
    global  _sol, _auxIni, _xdata, indexGrAux
    indexGrAux = 0
    updateCalculatedConstants()
    updateFunctions()
    
    print(_sol)
    print("-- Restart --")
    _sol = odeint(odesys, _auxIni, _xdata)
    print(_sol)


def getPoint():
    global _sol, indexGrAux
    #TODO calcular maximos y minimos por columna para graficar
    out = _sol[indexGrAux]
    indexGrAux += 1
    return out

