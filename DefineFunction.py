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


def defineParameters(constantTuples):
    constants = ""
    for c in constantTuples:
        constants += c.value1 + operators(c.operator) + c.value2 + "\n"
    return constants

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
