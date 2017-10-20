import libsbml as libsbml
import csv
import xml.etree.ElementTree as ET
import collections
import re


class ModelParser():

    def __init__(self,ModelFileName,LanguageFileName,Language):
        #Open language file
        languageFile = open(LanguageFileName, 'rt')
        # Open model file
        modelFile = open(ModelFileName, 'rt')
        #Parse XML
        tree = ET.parse(ModelFileName)
        if Language != "":
            self.languageHash = self.parseLanguages(LanguageFileName, Language)
        else:
            #TODO: Hacer que el default language sea el primero de la lista
            self.languageHash = self.parseLanguages(LanguageFileName, "English")

        model = tree.getroot()

        #First we get model's general settings
        self.name = model.attrib['name']
        self.defaultLanguage = model.attrib['lang']
        self.simulationFrequency = model.attrib['frequencyHz']

        self.userDefinedParameters = self.parseUserDefinedParameters(model, self.languageHash)
        self.userDefinedTreatment = self.filterNonTreatments(self.userDefinedParameters)
        self.constants = self.parseConstants(model, self.languageHash)
        self.functions = self.parseFunction(model, self.languageHash)
        self.equations = self.parseEquations(model, self.languageHash)
        self.languages = self.obtainPossibleLanguages(LanguageFileName)
        languageFile.close()
        modelFile.close()

    def filterNonTreatments(self,userDefinedParameters):
        d = collections.deque()
        for u in userDefinedParameters:
            if u.graphAsTreatment == "True" or u.graphAsTreatment == "true":
                d.append(u)
        return d

    def parseLanguages(self,LanguageFileName, language):
        f = open(LanguageFileName, 'rt')
        dictionary = {}
        try:
            reader = csv.reader(f)
            rowNum = 0
            for row in reader:
                if rowNum == 0:
                    languageIndex = 0
                    _i = 0
                    for cell in row:
                        if cell == language:
                            languageIndex = _i
                        _i = _i + 1
                else:
                    dictionary[row[0]] = row[languageIndex]
                rowNum = rowNum + 1
            return dictionary
        finally:
            f.close()

    def obtainPossibleLanguages(self,LanguageFileName):
        f = open(LanguageFileName, 'rt')
        try:
            reader = csv.reader(f)
            firstRow = next(reader)
            d = collections.deque()
            _i = 0
            for cell in firstRow:
                if _i > 0:  # First column is not a language
                    d.append(cell)
                _i = _i + 1
            return d
        finally:
            f.close()

    def parseConstants(self,xmlroot, languageHash):
        constants = xmlroot.find('parameters').find('constants')
        Constant = collections.namedtuple('Constant',['name', 'description', 'unit', 'calculated', 'value1', 'operator', 'value2'])
        d = collections.deque()
        for cons in constants:
            name = cons.attrib['name']

            if cons.attrib['description'].startswith("lbl."):
                description = languageHash[cons.attrib['description']]
            else:
                description = cons.attrib['description']

            if cons.attrib['unit'].startswith("lbl."):
                unit = languageHash[cons.attrib['unit']]
            else:
                unit = cons.attrib['unit']

            calculated = self.str_to_bool(cons.attrib['calculated'])
            xmlstr = ET.tostring(cons[0], encoding='unicode', method='xml')
            operation = self.translateMathML(xmlstr)
            matchObj = re.match(r'(.*?)\((.*?), (.*)\)', operation, re.M | re.I)
            c = Constant(name, description, unit, calculated, matchObj.group(2), matchObj.group(1), matchObj.group(3))
            d.append(c)
        return d

    def parseUserDefinedParameters(self,xmlroot, languageHash):
        userDefinedParameters = xmlroot.find('parameters').find('userDefinedParameters')
        UserDefined = collections.namedtuple('UserDefined',
                                             ['name', 'description', 'unit', 'type', 'defaultValue', 'isSlider',
                                              'sliderMin', 'sliderMax','graphAsTreatment'])
        d = collections.deque()
        for userdp in userDefinedParameters:
            name = userdp.attrib['name']
            graphAsTreatment = userdp.attrib['graphAsTreatment']
            if userdp.attrib['description'].startswith("lbl."):
                description = languageHash[userdp.attrib['description']]
            else:
                description = userdp.attrib['description']

            if userdp.attrib['unit'].startswith("lbl."):
                unit = languageHash[userdp.attrib['unit']]
            else:
                unit = userdp.attrib['unit']

            type = userdp.attrib['type']
            defaultValue = userdp.attrib['defaultValue']
            isSlider = False
            sliderMin = 0
            sliderMax = 0
            if userdp.attrib['slider'] == 'True' or userdp.attrib['slider'] == 'true':
                isSlider = True
                sliderMin = float(userdp.attrib['sliderMin'])
                sliderMax = float(userdp.attrib['sliderMax'])

            u = UserDefined(name, description, unit, type, defaultValue, isSlider, sliderMin, sliderMax,graphAsTreatment)
            d.append(u)
        return d

    def parseFunction(self, xmlroot, languageHash):
        functions = xmlroot.find('functions')
        Function = collections.namedtuple('Function', ['name', 'description', 'parameters','outputType','function'])
        d = collections.deque()
        for func in functions:
            xmlstr = ET.tostring(func, encoding='utf8', method='xml')

            if func.attrib['description'].startswith("lbl."):
                description = languageHash[func.attrib['description']]
            else:
                description = func.attrib['description']

            name = func.attrib['name']
            parameters = func.attrib['parameters']
            if ('outputType' in func.attrib):
                outputType = func.attrib['outputType']
            else:
                outputType = ""
            function = self.translateMathML(ET.tostring(func[0], encoding='unicode', method='xml'))
            f = Function(name, description, parameters,outputType, function)
            d.append(f)
        return d

    def str_to_bool(self,s):
        if s == 'True' or s == 'true':
            return True
        elif s == 'False' or s == 'false':
            return False
        else:
            raise ValueError  # evil ValueError that doesn't tell you what the wrong value was

    def parseEquations(self, xmlroot, languageHash):
        equations = xmlroot.find('equations')
        Equation = collections.namedtuple('Equation',
                                          ['name', 'description', 'unit', 'defaultValue', 'simulate', 'equation'])
        d = collections.deque()
        for eq in equations:
            name = eq.attrib['name']

            if eq.attrib['description'].startswith("lbl."):
                description = languageHash[eq.attrib['description']]
            else:
                description = eq.attrib['description']

            if eq.attrib['unit'].startswith("lbl."):
                unit = languageHash[eq.attrib['unit']]
            else:
                unit = eq.attrib['unit']

            defaultValue = eq.attrib['defaultValue']
            simulate = self.str_to_bool(eq.attrib['simulate'])
            equation = self.translateMathML(ET.tostring(eq[0], encoding='unicode', method='xml'))
            e = Equation(name, description, unit, defaultValue, simulate, equation)
            d.append(e)
        return d



    #
    # Translates the given infix formula into MathML.
    #
    # @return the MathML as a string.  The caller owns the memory and is
    # responsible for freeing it.
    #
    def translateInfix(self,formula):
        math = self.parseFormula(formula);
        return self.writeMathMLToString(math);

    #
    # Translates the given MathML into an infix formula.  The MathML must
    # contain no leading whitespace, but an XML header is optional.
    #
    # @return the infix formula as a string.  The caller owns the memory and
    # is responsible for freeing it.
    #
    def translateMathML(self,xml):
        math = libsbml.readMathMLFromString(xml)
        return libsbml.formulaToString(math)
