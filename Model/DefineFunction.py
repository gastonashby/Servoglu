
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
                    "self.model." + u.name + " = int_value / 100\n\t" \
                    "self.window.ui.dck_treat_controls.label[" + str(i - 1) + "]" \
                    ".setText('" + u.description + " ' + str(eval('self.model." + u.name + "')) + ' " + u.unit + "')\n\t" \
                    "self.model.recalculate(self.window.step)\n"

        _s_f_aux = "sliderValueChanged" + str(i)

        return sliderF, "self." + _s_f_aux + " = self.window.types.MethodType(" + _s_f_aux + ", self)", "self." + _s_f_aux
