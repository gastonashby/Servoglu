import os
import os.path
import numpy as np
from libsbml import *
import xml.etree.ElementTree as ET
import collections


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


def geq(x, y):
    return x >= y


def leq(x, y):
    return x <= y


def operators(op):
    if (op == "eq"):
        return "="


def log(x):
    return np.log(x)


def root(x, y):
    return np.power(y, 1 / x)


def operators(op):
    if (op == "eq"):
        return "="


def defineFunctions(functionTuples):
    functions = ""
    for f in functionTuples:
        functions += """def """ + f.name + """(""" + f.parameters + """):
                          return """ + f.function + """ \n"""
    return functions

# Recursive function to return the list of complete parameters
# If a function parameter is a function, call processParameters
def processParameters(funcList, params, _i):
    out = '('
    listPar =  params[_i].split(",")
    cantParam = len(listPar)
    _i = 0
    for par in listPar:
        out += par
        if par in funcList:
            j = funcList.index(par)
            out += processParameters(funcList, params, j)

        if _i < cantParam-1:
            out += ', '

        _i += 1
    out += ')'
    return out

def defineFunctionList(functionTuples):
    functions = []
    params = []
    for f in functionTuples:
        functions.append(f.name)
        params.append(f.parameters)

    pParams = []
    _i = 0
    for p in params:
        pParams.append(processParameters(functions, params, _i))
        _i += 1

    return functions, pParams


def defineParameters(constantTuples):
    constants = ""
    calculated = []
    for c in constantTuples:
        constants += c.value1 + operators(c.operator) + c.value2 + "\n"
        if c.calculated:
            calculated.append(c.value1 + operators(c.operator) + c.value2)
    return constants, calculated

def defineUserDefinedParameters(userDefinedTuples):
    userDefinedParameters = ""
    for u in userDefinedTuples:
        userDefinedParameters += u.name + " = " + u.defaultValue + "\n"
    return userDefinedParameters

def defineEquations(equationTuples):
    equations = ""
    noms = "_aux = ["
    # x = 2.0
    # y = 3.0
    # z = 4.0
    # aux = [x, y, z]
    for e in equationTuples:
        equations += e.name + " = " + e.defaultValue + "\n"
        noms += e.name + ","
    noms = noms[:len(noms) - 1]
    noms += "]"
    return equations + "\n" + noms
