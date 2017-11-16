
class DefiniteFunction:

    def __init__(self):
        pass


    def operators(self, op):
        if (op == "eq"):
            return "="

            # Recursive function to return the list of complete parameters

    # If a function parameter is a function, call processParameters
    def processParameters(self, funcList, params, _i):
        out = '('
        listPar = params[_i].split(",")
        cantParam = len(listPar)
        _i = 0
        for par in listPar:
            out += par
            if par in funcList:
                j = funcList.index(par)
                out += self.processParameters(funcList, params, j)

            if _i < cantParam - 1:
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

        return functions, params

    def defineFunctions(self, functionTuples, parameters):
        functions = ""
        definitions = ""
        i = 0
        for f in functionTuples:
            definitions +=  "self." + f.name + " = types.MethodType(" + f.name + ", self)\n"
            if (f.outputType == ''):
                if f.parameters == '':
                    functions += """def """ + f.name + """(self): return """ \
                                 + self.process(f.function, parameters[0]) + """ \n"""
                else:
                    functions += """def """ + f.name + """(self, """ + f.parameters + """):return """ \
                                 + self.process(f.function, parameters[0]) + """ \n"""
            else:
                functions += """def """ + f.name + """(self, """ + f.parameters + """):return """ \
                             + f.outputType + """(""" + self.process(f.function, parameters[0]) + """)""" +""" \n"""
            i += 1
        return functions, definitions

    def processEq(self, str):
        listW = str.replace('(', '( ').split(' ')
        listN = []
        for w in listW:
            if w[0].isalpha():
                listN.append('self.' + w)
            elif w[0] == "-" and len(w) > 1 and w[1].isalpha():
                listN.append('-self.' + w[1:])
            else:
                listN.append(w)
        return ' '.join(listN)

    def process(self, str, funcList):
        listW = str.replace('(', '( ').split(' ')
        listN = []
        for w in listW:
            pos = -1
            for i, j in enumerate(funcList):
                if j == w.replace("(", "").replace(")", "").replace("-", ""):
                    pos = i

            if pos != -1:
                if w[0] == "-":
                    listN.append('-self.' + w[1:])
                else:
                    listN.append('self.' + w)
            elif w[0].isalpha():
                listN.append('self.' + w)
            elif w[0] == "-" and len(w) > 1 and w[1].isalpha():
                listN.append('-self.' + w[1:])
            else:
                listN.append(w)
        return ' '.join(listN)

    def defineParameters(self, constantTuples, parameters):
        constants = ""
        calculated = []
        for c in constantTuples:
            constants += 'self.' + c.value1 + self.operators(c.operator) + \
                         self.process(c.value2, parameters[0]) + "\n"
            if c.calculated:
                calculated.append("self." + c.value1 + self.operators(c.operator) +
                                  self.process(c.value2, parameters[0]))
        return constants, calculated


    def defineUserDefinedParameters(self, userDefinedTuples, funcList):
        userDefinedParameters = ""
        for u in userDefinedTuples:
            val = None
            if u.defaultValue[0].isalpha() or \
                    (u.defaultValue[0] == '-' and len(u.defaultValue) > 1 and u.defaultValue[1].isalpha()):
                val = self.process(u.defaultValue, funcList[0] + "/" + str(u.convertFactor))
            else:
                val = str(float(u.defaultValue) / u.convertFactor)

            userDefinedParameters += "self." + u.name + " = " + val + "\n"
        return userDefinedParameters


    def defineEquations(self, equationTuples, funcList):
        equations = ""
        noms = "self._aux = ["
        # x = 2.0
        # y = 3.0
        # z = 4.0
        # aux = [x, y, z]
        for e in equationTuples:
            if e.defaultValue[0].isalpha()or \
                    (e.defaultValue[0] == '-' and len(e.defaultValue) > 1 and e.defaultValue[1].isalpha()):
                equations += "self." + e.name + " = (" \
                             + self.process(e.defaultValue, funcList[0]) + ") / " + str(e.convertFactor) + "\n"
            else:
                equations += "self." + e.name + " = " \
                             + str(float(e.defaultValue) / e.convertFactor) + "\n"
            noms += "self." + e.name + ","
        noms = noms[:len(noms) - 1]
        noms += "]"
        return equations + "\n" + noms

    def definiteSlider(self, u, i, convertFactor):
        sliderF = "def sliderValueChanged" + str(i) + "(self, int_value):\n\t" \
                    "new_val = int_value / " + str(convertFactor) + "\n\t" \
                    "print(new_val / 100)\n\t" \
                    "self.model." + u.name + " = new_val / 100 \n\t" \
                    "self.window.ui.dck_treat_controls.label[" + str(i - 1) + "]" \
                    ".setText('" + u.description + " ' + str(int_value/100) + ' " + u.unit + "')\n\t" \
                    "self.model.recalculate(self.window.step)\n"

        _s_f_aux = "sliderValueChanged" + str(i)

        #print (sliderF, "self." + _s_f_aux + " = self.window.types.MethodType(" + _s_f_aux + ", self)", "self." + _s_f_aux)
        return sliderF, "self." + _s_f_aux + " = self.window.types.MethodType(" + _s_f_aux + ", self)", "self." + _s_f_aux
