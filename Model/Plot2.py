
#import ParsingMathML as mp
import numpy as np
import sys
import Model.DefineFunction as df
import Model.ModelParser as mp


def piecewise(*args):
    trueIndex = 0
    for index, obj in enumerate(args):
        if obj == True:
            trueIndex = index
    return args[trueIndex - 1]

def lt(x, y):
    return x < y

def gt(x, y):
    return x > y


def eq(x, y):
    return x == y

def neq(x, y):
    return x != y

def geq(x, y):
    return x >= y


def leq(x, y):
    return x <= y


def log(x):
    return np.log(x)


def root(x, y):
    return np.power(y, 1 / x)

def quotient(x, y):
    return x % y

from scipy.integrate import odeint

_u = []
_t = []
_c = []
_f = []
_e = []
_sol = [0]
_constants = []
_calculated = []
indexGrAux = 0
modelTime = 0
top_x = 100
_xdata = np.arange(0, top_x - 1, 1)
gen = []
plt_step = 0
language = ""
timeUnit = ""

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


def initialize(name, step):
    global _u, _t, _c, _f, _e, _timeUnit, _constants, _calculated, _sol, _aux, _xdata, _auxIni, gen, indexGrAux, simulatedModel,language, plt_step
    indexGrAux = 0
    plt_step = step
    # model = mp.ModelParser('Pharmacokinetics.xml', 'LanguageSupport.csv')

    simulatedModel = mp.ModelParser(name, 'LanguageSupport.csv',language)


    _u = simulatedModel.userDefinedParameters
    _t = simulatedModel.userDefinedTreatment
    _c = simulatedModel.constants
    _f = simulatedModel.functions
    _e = simulatedModel.equations
    _timeUnit = simulatedModel.timeUnit

    gen = df.DefiniteFunction()

    #print(_e)

    exec(gen.defineUserDefinedParameters(_u), globals())
    _constants, _calculated = gen.defineParameters(_c)
    exec(_constants, globals())
    # _functionList, _paramsList = defineFunctionList(_f)
    exec(gen.defineFunctions(_f), globals())
    exec(gen.defineEquations(_e), globals())
    _auxIni = _aux
    _sol = odeint(odesys, _aux, _xdata)
    print('Solution created 1st time')
    #print(_sol[:100])


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

def change_scale(step, init):
    global _xdata, indexGrAux, plt_step
    #TODO dtype
    _xdata = np.linspace(init, init + (top_x - 1) * step, top_x)
    plt_step = step
    #print("plt2 ", _xdata[:indexGrAux + 10])

def recalculate(step):
    global _sol, _aux, _xdata, indexGrAux, _c, top_x
    _aux = _sol[indexGrAux-1]
    #print(_xdata)
    _xdata = np.linspace(_xdata[indexGrAux-1],
                    _xdata[indexGrAux-1] + (top_x - 1) * step, top_x)
    #print(_xdata)
    indexGrAux = 1
    updateCalculatedConstants()

#    updateFunctions()
    #print(_aux)
    #print(_sol[:indexGrAux + 10])
    print("-- Recalculate --")
    _sol = odeint(odesys, _aux, _xdata)
    #print(_sol[:indexGrAux + 10])


def restart():
    global _sol, _auxIni, _xdata, indexGrAux
    indexGrAux = 0
    updateCalculatedConstants()
 #   updateFunctions()
    #print(_sol[:indexGrAux + 10])
    print("-- Restart --")
    _sol = odeint(odesys, _auxIni, _xdata)
    #print(_sol[:indexGrAux + 10])


def getPoint():
    global _sol, indexGrAux, top_x, plt_step
    #TODO calcular maximos y minimos por columna para graficar
    # print("indexGrAux", indexGrAux)
    if indexGrAux == top_x - 1:
        #TODO pasarle los valores iniciales para recalcular el eje x
        recalculate(plt_step)

    out = _sol[indexGrAux]
    indexGrAux += 1
    return out

