import csv
import xml.etree.ElementTree as ET
import collections
import re

class LanguageParser():

    def __init__(self,LanguageFileName,Language):
        self.languageFileName = LanguageFileName
        self.languageHash = self.parseLanguages(self.languageFileName, Language)
        self.languages = self.obtainPossibleLanguages()

    def parseLanguages(self,LanguageFileName, Language):
        # Open language file
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
                        if cell == Language:
                            languageIndex = _i
                        _i = _i + 1
                else:
                    dictionary[row[0]] = row[languageIndex]
                rowNum = rowNum + 1
            return dictionary
        finally:
            f.close()

    def obtainPossibleLanguages(self):
        f = open(self.languageFileName, 'rt')
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

    def changeLanguage(self,NewLanguage):
        self.languageHash = self.parseLanguages(self.languageFileName, NewLanguage)

