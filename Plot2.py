
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
    # _globals = []
    # for _const in _calculated:
    #     _globals.append(_const.split("=")[0])
    #
    # print("global " + ", ".join(_globals))
    # exec("global " + ", ".join(_globals), globals())

    for _i in range(0, len(_calculated)-1):
        #print(eval(_calculated[_i]))
        print(_calculated[_i])
        exec(_calculated[_i], globals())
    print(eval("ABSA"))

def updateFunctions():
    for _i in range(0, len(_functionList)-1):
        #print(eval(_functionList[_i] + _paramsList[_i]))
        print(_functionList[_i] + _paramsList[_i])
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

#print(_xdata)
_y = odeint(fGluc, _aux, _xdata)
print('Solution created 1st time')


def recalculate1():
    global indexGrAux
    #print('5')
    recalculate(indexGrAux)


def recalculate(indexGr):
    global _y, _aux, _xdata, indexGrAux, _c
    _globals = []
    # for _const in _calculated:
    #     _globals.append(_const.split("=")[0])
    #
    # exec("global " + ", ".join(_globals), globals())
    # print("global " + ", ".join(_globals))


    _aux = _y[indexGr]
    #print(eval("ABSA"))
    #for const in _c:
    #    if const.calculated:
    #        print(const.value1 + operators(const.operator) + const.value2)
    #        exec(const.value1 + operators(const.operator) + const.value2, globals())
    #print(eval("ABSA"))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    updateCalculatedConstants()
    print(eval("ABSA"))
    updateFunctions()
    indexGrAux = 0
    print("*********")
    print(_y)
    print("----")
    _y = odeint(fGluc, _aux, _xdata)
    print(_y)



def restart():
    global  _y, _auxIni, _xdata
    #_xdata = np.linspace(0, 999, 1000)
    _y = odeint(fGluc, _auxIni, _xdata)


def obtener(_i):
    global _y
    #print('2')
    #print(_i)
    #print(_y)
    return _y[_i]

