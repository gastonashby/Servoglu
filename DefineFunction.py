
class DefiniteFunction():

    def __init__(self):
        pass


    def operators(self, op):
        if (op == "eq"):
            return "="


    def defineFunctions(self, functionTuples):
        functions = ""
        for f in functionTuples:
            if (f.outputType == ''):
                functions += """def """ + f.name + """(""" + f.parameters + """):
                              return """ + f.function + """ \n"""
            else:
                functions += """def """ + f.name + """(""" + f.parameters + """):
                              return """ + f.outputType + """(""" + f.function + """)""" +""" \n"""
        return functions

    # Recursive function to return the list of complete parameters
    # If a function parameter is a function, call processParameters
    def processParameters(self, funcList, params, _i):
        out = '('
        listPar =  params[_i].split(",")
        cantParam = len(listPar)
        _i = 0
        for par in listPar:
            out += par
            if par in funcList:
                j = funcList.index(par)
                out += self.processParameters(funcList, params, j)

            if _i < cantParam-1:
                out += ', '

            _i += 1
        out += ')'
        return out

    def defineFunctionList(self, functionTuples):
        functions = []
        params = []
        for f in functionTuples:
            functions.append(f.name)
            params.append(f.parameters)

        pParams = []
        _i = 0
        for p in params:
            pParams.append(self.processParameters(functions, params, _i))
            _i += 1

        return functions, pParams


    def defineParameters(self, constantTuples):
        constants = ""
        calculated = []
        for c in constantTuples:
            constants += c.value1 + self.operators(c.operator) + c.value2 + "\n"
            if c.calculated:
                calculated.append(c.value1 + self.operators(c.operator) + c.value2)
        return constants, calculated


    def defineUserDefinedParameters(self, userDefinedTuples):
        userDefinedParameters = ""
        for u in userDefinedTuples:
            userDefinedParameters += u.name + " = " + u.defaultValue + "\n"
        return userDefinedParameters


    def defineEquations(self, equationTuples):
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

    def definiteSlider(self, u, i):
        sliderF = "def sliderValueChanged" + str(i) + "(self, int_value):\n\tprint(int_value / 100)\n\t" \
                    "plt2." + u.name + " = int_value / 100\n\tself.ui.dck_model_param_controls.label[" \
                    + str(i - 1) + "]" \
                    ".setText('" + u.description + " ' + str(eval('plt2." + u.name + "')) + ' " + u.unit + "')\n\t" \
                    "plt2.recalculate()\n"

        _s_f_aux = "sliderValueChanged" + str(i)

        return sliderF, "self." + _s_f_aux + " = types.MethodType(" + _s_f_aux + ", self)", "self." + _s_f_aux
