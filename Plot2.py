
#import ParsingMathML as mp
from DefineFunction import *

import numpy as np
import ModelParser as mp

from scipy.integrate import odeint

_u = []
_c = []
_f = []
_e = []
_sol = [0]
_constants = []
_calculated = []
indexGrAux = 0
modelTime = 0
top_x = 100
_xdata = np.linspace(0, top_x - 1, top_x, dtype=np.int32)


def odesys(XX,  tt):
    global _e
    global modelTime
    modelTime = int(tt)
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


def initialize(name):
    global _u, _c, _f, _e, _constants, _calculated, _sol, _aux, _xdata, _auxIni
    # model = mp.ModelParser('Pharmacokinetics.xml', 'LanguageSupport.csv')
    model = mp.ModelParser(name, 'LanguageSupport.csv')
    _u = model.userDefinedParameters
    _c = model.constants
    _f = model.functions
    _e = model.equations

    print (_e)

    exec(defineUserDefinedParameters(_u), globals())
    _constants, _calculated = defineParameters(_c)
    exec(_constants, globals())
    # _functionList, _paramsList = defineFunctionList(_f)
    exec(defineFunctions(_f), globals())
    exec(defineEquations(_e), globals())
    _auxIni = _aux
    _sol = odeint(odesys, _aux, _xdata)
    print('Solution created 1st time')
    print(_sol)


def updateCalculatedConstants():
    for _i in range(0, len(_calculated)-1):
        #print(eval(_calculated[_i]))
        #print(_calculated[_i])
        exec(_calculated[_i], globals())
    #print(eval("ABSA"))

# def updateFunctions():
#     for _i in range(0, len(_functionList)-1):
#         #print(eval(_functionList[_i] + _paramsList[_i]))
#         #print(_functionList[_i] + _paramsList[_i])
#         eval(_functionList[_i] + _paramsList[_i])

def change_scale(step):
    global _xdata, indexGrAux
    _xdata = np.linspace(0, (top_x - 1) * step, top_x)
    print("plt2 ", _xdata[:indexGrAux + 10])

def recalculate():
    global _sol, _aux, _xdata, indexGrAux, _c
    _aux = _sol[indexGrAux-1]
    indexGrAux = 1
    updateCalculatedConstants()
#    updateFunctions()
    print(_sol)
    print("-- Recalculate --")
    _sol = odeint(odesys, _aux, _xdata)
    print(_sol)


def restart():
    global _sol, _auxIni, _xdata, indexGrAux
    indexGrAux = 0
    updateCalculatedConstants()
 #   updateFunctions()
    print(_sol)
    print("-- Restart --")
    _sol = odeint(odesys, _auxIni, _xdata)
    print(_sol)


def getPoint():
    global _sol, indexGrAux, top_x
    #TODO calcular maximos y minimos por columna para graficar
    # print("indexGrAux", indexGrAux)
    if indexGrAux == top_x - 2:
        recalculate()

    out = _sol[indexGrAux]
    indexGrAux += 1
    return out

