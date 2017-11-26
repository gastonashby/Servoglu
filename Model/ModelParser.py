import libsbml as libsbml
import csv
import xml.etree.ElementTree as ET
import collections
import re
import os


class ModelParser():

    def __init__(self,ModelFileName,Language):

        # Open model file
        modelFile = open(ModelFileName, 'rt')
        #Parse XML
        try:
            tree = ET.parse(ModelFileName)
        except Exception as e:
            raise Exception('Error parsing XML.')

        model = tree.getroot()

        #First we get model's general settings
        self.name = model.attrib['name']
        self.defaultLanguage = model.attrib['lang']
        self.timeUnit = model.attrib['timeUnit']

        #Empieza a procesar lenguaje del modelo
        if ('languageSupport' in model.attrib):
            self.languageSupport = model.attrib['languageSupport']

            modelDir = os.path.dirname(ModelFileName)
            self.languageFileDir = modelDir +'/'+ self.languageSupport

            self.languages = self.obtainPossibleLanguages()

            if Language != "":
                self.languageHash = self.parseLanguages(Language)
            else:
                # TODO: Hacer que el default language sea el primero de la lista
                self.languageHash = self.parseLanguages("English")

        ##Termino de procesar lenguaje del modelo

        if ('template' in model.attrib):
            self.template = model.attrib['template']
        else:
            self.template = "template.html" #Default template

        self.userDefinedParameters = self.parseUserDefinedParameters(model, self.languageHash)
        self.userDefinedTreatment = self.filterNonTreatments(self.userDefinedParameters)
        self.constants = self.parseConstants(model, self.languageHash)
        self.functions = self.parseFunction(model, self.languageHash)
        self.equations = self.parseEquations(model, self.languageHash)

        modelFile.close()

    def filterNonTreatments(self,userDefinedParameters):
        d = collections.deque()
        for u in userDefinedParameters:
            if u.graphAsTreatment:
                d.append(u)
        return d

    def parseLanguages(self,language):
        try:
            languageFile = open(self.languageFileDir, 'rt')
            dictionary = {}
            reader = csv.reader(languageFile)
            rowNum = 0
            for row in reader:
                if rowNum == 0:
                    languageIndex = 0
                    _i = 0
                    for cell in row:
                        if cell == language:
                            languageIndex = _i
                        _i = _i + 1
                elif len(row) > 0:  # se saltea la primera linea
                    dictionary[row[0]] = row[languageIndex]
                rowNum = rowNum + 1
            return dictionary
        finally:
            languageFile.close()


    def obtainPossibleLanguages(self):
        try:
            languageFile = open(self.languageFileDir, 'rt')
            reader = csv.reader(languageFile)
            firstRow = next(reader)
            d = collections.deque()
            _i = 0
            for cell in firstRow:
                if _i > 0:  # First column is not a language
                    d.append(cell)
                _i = _i + 1
            return d
        finally:
            languageFile.close()


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
                                              'minTreatment', 'maxTreatment', 'graphAsTreatment', 'convertFactor',
                                              'detailedDescription', 'color'])
        d = collections.deque()
        for userdp in userDefinedParameters:
            name = userdp.attrib['name']
            graphAsTreatment = False
            isSlider = False
            trMin = []
            trMax = []
            type = userdp.attrib['type']
            graphAsTreatment = []

            if 'graphAsTreatment' in userdp.attrib:
                graphAsTreatment = self.str_to_bool(userdp.attrib['graphAsTreatment'])
                if graphAsTreatment:
                    if 'slider' in userdp.attrib and \
                                    userdp.attrib['slider'] == 'True' or userdp.attrib['slider'] == 'true':
                        isSlider = True

                    if type == "int" or type == "integer":
                        trMin = int(userdp.attrib['minTreatment'])
                        trMax = int(userdp.attrib['maxTreatment'])
                    else:
                        trMin = float(userdp.attrib['minTreatment'])
                        trMax = float(userdp.attrib['maxTreatment'])

            detailedDescription = ""
            if 'detailedDescription' in userdp.attrib:
                if userdp.attrib['detailedDescription'].startswith("lbl."):
                    detailedDescription = languageHash[userdp.attrib['detailedDescription']]
                else:
                    detailedDescription = userdp.attrib['detailedDescription']

            if userdp.attrib['description'].startswith("lbl."):
                description = languageHash[userdp.attrib['description']]
            else:
                description = userdp.attrib['description']

            if userdp.attrib['unit'].startswith("lbl."):
                unit = languageHash[userdp.attrib['unit']]
            else:
                unit = userdp.attrib['unit']


            defaultValue = userdp.attrib['defaultValue']


            convertFactor = 1
            if 'convertFactor' in userdp.attrib:
                convertFactor = float(userdp.attrib['defaultValue'])

            color = ""
            if 'color' in userdp.attrib:
                color = userdp.attrib['color']

            u = UserDefined(name, description, unit, type, defaultValue, isSlider, trMin, trMax,
                            graphAsTreatment, convertFactor, detailedDescription, color)
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
                                          ['name', 'description', 'unit', 'defaultValue', 'simulate', 'equation',
                                           'convertFactor', 'detailedDescription', 'alMinVal', 'alMaxVal',
                                           'alDescription'])
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

            convertFactor = 1
            if 'convertFactor' in eq.attrib:
                convertFactor = float(eq.attrib['convertFactor'])

            defaultValue = eq.attrib['defaultValue']
            simulate = self.str_to_bool(eq.attrib['simulate'])
            equation = self.translateMathML(ET.tostring(eq[0], encoding='unicode', method='xml'))

            detailedDescription = ""
            if 'detailedDescription' in eq.attrib:
                if eq.attrib['detailedDescription'].startswith("lbl."):
                    detailedDescription = languageHash[eq.attrib['detailedDescription']]
                else:
                    detailedDescription = eq.attrib['detailedDescription']

            alMinVal = None
            alMaxVal = None
            alDescription = ""

            if 'alarmDescription' in eq.attrib:
                if eq.attrib['alarmDescription'].startswith("lbl."):
                    alDescription = languageHash[eq.attrib['alarmDescription']]
                else:
                    alDescription = eq.attrib['alarmDescription']

            if 'alarmMinVal' in eq.attrib:
                if 'alarmMinVal' in eq.attrib:
                    alMinVal = float(eq.attrib['alarmMinVal'])

            if 'alarmDescription' in eq.attrib:
                if 'alarmMaxVal' in eq.attrib:
                    alMaxVal = float(eq.attrib['alarmMaxVal'])

            e = Equation(name, description, unit, defaultValue, simulate, equation, convertFactor, detailedDescription,
                         alMinVal, alMaxVal, alDescription)
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
