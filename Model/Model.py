
#import ParsingMathML as mp
import numpy as np
import sys
import Model.DefineFunction as df
import Model.ModelParser as mp
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from scipy.integrate import odeint
import math
#from Model.Utils import Utils
import types

class Model:

    def __init__(self):
        np.seterr(all='raise', divide='raise', over='raise', under='raise', invalid='raise')
        self._u = []
        self._t = []
        self._c = []
        self._f = []
        self._e = []
        self._sol = [0]
        self._constants = []
        self._calculated = []
        self.indexModel = 0
        self.modelTime = 0
        self.top_x = 100
        self._xdata = np.arange(0, self.top_x - 1, 1)
        self.code = []
        self.step = 0
        self.plt_step = 1
        self.language = ""
        self._timeUnit = ""
        self._modelName = ""
        self._template = ""

        self.np = np
        self.functions = []
        self.languages = []

    def odesys(self, XX, tt):

        self.modelTime = int(tt)
        _i = 0
        salida = []

        for ec in self._e:
            auux = "self." + ec.name + '= XX[' + str(_i) + ']'
            _i += 1
            exec (auux)

        for eq in self._e:
            salida.append(eval(self.code.processEq(eq.equation)))


        # print('t: ', self.modelTime,'e():', round(self.e(),5),'z:', self.z,'E():', round(self.E(),5),
        #       'Pglut4():', round(self.Pglut4(),5),'a():',
        #       round(self.a(),5),'iaster():', round(self.iaster(),5),
        #       'iaster0:', round(self.iaster0, 5),'pinicial0:', round(self.pInitial0, 5),
        #       'BG:', round(self.BG,5))
        return salida

    def initialize(self, name, step):
        self.indexModel = 0
        self.step = step
        self.plt_step = step
        simulatedModel = mp.ModelParser(name, self.language)

        self._u = simulatedModel.userDefinedParameters
        self._t = simulatedModel.userDefinedTreatment
        self._c = simulatedModel.constants
        self._f = simulatedModel.functions
        self._e = simulatedModel.equations
        self._timeUnit = simulatedModel.timeUnit
        self._modelName = simulatedModel.name
        self._template = simulatedModel.template
        self.languages = simulatedModel.languages

        self.code = df.DefiniteFunction()

        params = self.code.defineFunctionList(self._f)
        self.functions, definitions = self.code.defineFunctions(self._f, params)
        self._constants, self._calculated = self.code.defineParameters(self._c, params)

        exec(self.code.defineUserDefinedParameters(self._u, params))
        exec(self._constants)
        exec(self.code.defineEquations(self._e, params))
        exec(self.functions)
        exec(definitions)

        self._auxIni = self._aux
        self._sol = odeint(self.odesys, self._aux, self._xdata)
        print('Solution created 1st time')


    def updateCalculatedConstants(self):
        for _i in range(0, len(self._calculated)-1):
            exec(self._calculated[_i])

    def change_scale(self, step, init):
        self._xdata = np.linspace(init, init + (self.top_x - 1) * self.step, self.top_x)
        self.plt_step = self.step

    def recalculate(self, step):
        self._aux = self._sol[self.indexModel-1]
        self._xdata = np.linspace(self._xdata[self.indexModel-1],
                                  self._xdata[self.indexModel-1] + (self.top_x - 1) * self.step, self.top_x)
        self.indexModel = 1
        self.updateCalculatedConstants()

        print("-- Recalculate --")
        self._sol = odeint(self.odesys, self._aux, self._xdata)
        #print(self._sol)

    def change_val(self, i, val):
        self._sol[self.indexModel-1][i] = val

    def restart(self):
        self.indexModel = 0
        self.updateCalculatedConstants()
        print("-- Restart --")
        self._sol = odeint(self.odesys, self._auxIni, self._xdata)


    def getPoint(self):
        if self.indexModel == self.top_x - 1:
            self.recalculate(self.plt_step)

        out = self._sol[self.indexModel]
        self.indexModel += 1
        #return np.multiply(out, eq_convert_factors)
        return out


    def piecewise(self, *args):
        trueIndex = 0
        for index, obj in enumerate(args):
            if obj == True:
                trueIndex = index
        return args[trueIndex - 1]

    def lt(self, x, y):
        return x < y

    def gt(self, x, y):
        return x > y

    def eq(self, x, y):
        return x == y

    def neq(self, x, y):
        return x != y

    def geq(self, x, y):
        return x >= y

    def leq(self, x, y):
        return x <= y

    def log(self, x):
        return np.log(x)

    def root(self, x, y):
        return np.power(y, 1 / x)

    def quotient(self, x, y):
        return x % y

    def pow(self, x, y):
        try:
            if x < 0.00000001:
                return 0
            else:
                return pow(x, y)
        except Exception as e:
            print(e)
        return 0


    def max(self, *x):
        return max(x)

    def min(self, *x):
        return min(x)
