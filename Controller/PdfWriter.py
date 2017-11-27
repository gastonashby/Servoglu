import datetime
import numpy
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader, PdfFileWriter
from xhtml2pdf import pisa
import math
import locale



def generateMetaData(pdfTuple,equations,userDefinedParameters,constants,):
    templateFile = pdfTuple.templateFile
    # Generate PDF from a html file.
    with open(templateFile, 'r') as myfile:
        html = myfile.read().replace('\n', '')

    #['name', 'description', 'unit', 'defaultValue', 'equation','convertFactor', 'detailedDescription'])
    equationsDescription = "<strong>Equations:</strong> </br>"
    for e in equations:
        equationsDescription+= "d"+e.name+"/dt" + " : " + e.description + " (" + e.unit + ")" + "</br>"

    # ['name', 'description', 'unit', 'type', 'defaultValue','detailedDescription', 'color']
    userDefinedParamDesc = "<strong>Initial conditions:</strong> </br>"
    for u in userDefinedParameters:
        userDefinedParamDesc += u.description + " = " + u.defaultValue + " " + u.unit + "</br>"
    for e in equations:
        userDefinedParamDesc += "d"+e.name+"/dt" + " = " + e.defaultValue + " " + e.unit + "</br>"

    constantsDescription = "<strong>Constants:</strong> </br>"
    for c in constants:
        constantsDescription += c.name + " : " + c.value1 + " = " + c.value2 +"</br>"

    htmlVariables = replaceVariables(html,pdfTuple,equationsDescription,userDefinedParamDesc,constantsDescription)
    resultFile = open('meta.pdf', "w+b")

    # convert HTML to PDF
    pisa.CreatePDF(htmlVariables,dest=resultFile)
    # close output file
    resultFile.close()  # close output file


def replaceVariables(html,pdfTuple,equationsDescription,userDefinedParamDesc,constantsDescription):
    html = html.replace("{{patientName}}",pdfTuple.patientName)
    html = html.replace("{{patientAdditionalInfo}}", pdfTuple.patientAdditionalInfo)
    html = html.replace("{{technician}}", pdfTuple.technician)
    html = html.replace("{{simulationInfo}}", pdfTuple.simulationInfo)
    #Seteamos fecha en idioma local
    locale.setlocale(locale.LC_TIME, '')
    format = '%Y-%m-%d %I:%M %p'
    html = html.replace("{{date}}", datetime.datetime.now().strftime(format))
    html = html.replace("{{modelInfo}}",pdfTuple.modelInfo)
    html = html.replace("{{equations}}",equationsDescription)
    html = html.replace("{{userDefinedParameters}}", userDefinedParamDesc)
    html = html.replace("{{constants}}", constantsDescription)
    return html

def generatePlotsWithTreatment(simulatedEquations,simulatedTreatment,results,treatment,xData,equations,userDefined,pdfTuple):
    plotSections = pdfTuple.plotSections
    plotsPerPage = pdfTuple.plotsPerPage
    timeUnit = pdfTuple.timeUnit

    plotSize = math.ceil(xData.size / plotSections)
    grid_size = (plotsPerPage, 1)

    with PdfPages('plots.pdf') as pdf:
        plt.figure(figsize=(8.27, 11.69))
        equationsIndex = 0
        #Si hay solo una pagina el indice del tratamiento es 0
        if plotsPerPage == 1:
            treatmentsIndex = 0
        else:
            treatmentsIndex = 1

        plotCount = 0

        for i in range(0,plotSections):
            ###PLOT EQUATIONS####
            plt.subplot2grid(grid_size, (equationsIndex,0))
            j = 0
            for ec in equations:
                if simulatedEquations[j]: #si estaba activa la visualizacion de la grafica
                    plt.plot(xData[i*plotSize:(plotSize*(i+1))+1],
                             results[i*plotSize:(plotSize*(i+1))+1, j], label=ec.name +":"+ ec.description + " (" + ec.unit + ")")
                    #plt.xticks(numpy.arange(min(xData[i*plotSize:(plotSize*(i+1))+1]), max(xData[i*plotSize:(plotSize*(i+1))+1]) + 1, 1.0))
                    plotAlarms(plt, ec)
                j+=1

            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel("time"+"("+timeUnit+")") #TODO agregar unidad de tiempo en ejes y labels
            plt.grid(True)
            plt.title('Model Equations')
            equationsIndex += 2
            if (equationsIndex > plotsPerPage - 1):
                equationsIndex = 0
            plotCount +=1

            #####PLOT TREATMENT
            #Si termino la pagina y lo ultimo que imprimio fue una ecuacion
            if (plotCount % plotsPerPage == 0):
                plt.tight_layout()
                pdf.savefig()  # saves the current figure into a pdf page
                plt.clf()  # clean page
                treatmentsIndex = 0
                if (plotsPerPage == 1):
                    equationsIndex = 0
                else:
                    equationsIndex = 1

            h =0
            plt.subplot2grid(grid_size, (treatmentsIndex,0))
            for u in userDefined:
                if simulatedTreatment[h]:
                    plt.plot(xData[i * plotSize:(plotSize * (i + 1)) + 1],
                             treatment[i * plotSize:(plotSize * (i + 1)) + 1, h], label=u.description + " (" + u.unit + ")")
                    #plt.xticks(numpy.arange(min(xData[i * plotSize:(plotSize * (i + 1)) + 1]),
                    #                        max(xData[i * plotSize:(plotSize * (i + 1)) + 1]) + 1, 1.0))
                h += 1
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel("time" + "(" + timeUnit + ")")
            plt.title('Simulated treatment')
            plt.grid(True)
            treatmentsIndex += 2
            if (treatmentsIndex > plotsPerPage - 1):
                if plotsPerPage == 1:
                    treatmentsIndex = 0
                else:
                    treatmentsIndex = 1
            plotCount += 1

            if (plotCount % plotsPerPage == 0):
                plt.tight_layout()
                pdf.savefig()  # saves the current figure into a pdf page
                plt.clf()  # clean page

        if (plotCount % plotsPerPage != 0):
            plt.tight_layout()
            pdf.savefig()  # saves the current figure into a pdf page

        plt.close()


def generatePlots(simulatedEquations,results,xData,equations,pdfTuple):
    plotSections = pdfTuple.plotSections
    plotsPerPage = pdfTuple.plotsPerPage
    timeUnit = pdfTuple.timeUnit

    plotSize = math.ceil(xData.size / plotSections)
    grid_size = (plotsPerPage, 1)

    with PdfPages('plots.pdf') as pdf:
        plt.figure(figsize=(8.27,8.27))

        equationsIndex = 0
        plotCount = 0

        for i in range(0,plotSections):
            ###PLOT EQUATIONS####
            plt.subplot2grid(grid_size, (equationsIndex,0))
            j = 0
            for ec in equations:
                if simulatedEquations[j]:
                    plt.plot(xData[i*plotSize:(plotSize*(i+1))+1], results[i*plotSize:(plotSize*(i+1))+1, j],
                             label=ec.description + " (" + ec.unit + ")")
                    plotAlarms(plt,ec)
                    #plt.xticks(numpy.arange(min(xData[i * plotSize:(plotSize * (i + 1)) + 1]),
                    #                        max(xData[i * plotSize:(plotSize * (i + 1)) + 1]) + 1, 1.0))
                j+=1


            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel("time" + "(" + timeUnit + ")")
            plt.title('Model Equations')
            plt.grid(True)
            equationsIndex += 1
            if (equationsIndex > plotsPerPage - 1):
                equationsIndex = 0
            plotCount +=1

            if (plotCount % plotsPerPage == 0):
                plt.tight_layout()
                pdf.savefig() # saves the current figure into a pdf page
                plt.clf() # clean page


        if (plotCount % plotsPerPage != 0):
            plt.tight_layout()
            pdf.savefig()  # saves the current figure into a pdf page

        plt.close()

def plotAlarms(plot,ec):
    if (ec.alMaxVal != None):
        plt.axhline(y=ec.alMaxVal, linestyle='dashed', linewidth=0.7,
                    label=ec.name + " alarm max/min value")
    if (ec.alMinVal != None) and (
                ec.alMaxVal != None):  # Se imprime solo una vez el label(el del max o min)
        plt.axhline(y=ec.alMinVal, linestyle='dashed', linewidth=0.7)
    elif (ec.alMinVal != None):  # Se imprime solo una vez el label(el del max o min)
        plt.axhline(y=ec.alMinVal, linestyle='dashed', linewidth=0.7,
                    label=ec.name + " alarm max/min value")



# Creating a routine that appends files to the output file
def append_pdf(input, output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

def mergePdfs(fileName):
    # Creating an object where pdf pages are appended to
    output = PdfFileWriter()
    # Appending two pdf-pages from two different files
    with open("meta.pdf", "rb") as meta:
        with open("plots.pdf", "rb") as plots:
            with open(fileName, "wb") as merged:
                append_pdf(PdfFileReader(meta), output)
                append_pdf(PdfFileReader(plots), output)
                # Writing all the collected pages to a file
                output.write(merged)



def createPdf(simulatedEquations,simulatedTreatment,results,treatment,xData,
              equations,userDefinedTreatment,userDefinedParameters,constants,pdfTuple):

    generateMetaData(pdfTuple,equations,userDefinedParameters,constants)

    if (len(treatment) > 0):
        generatePlotsWithTreatment(simulatedEquations,simulatedTreatment,results, treatment, xData, equations, userDefinedTreatment,pdfTuple)
    else:
        generatePlots(simulatedEquations,results, xData, equations,pdfTuple)
    mergePdfs(pdfTuple.fileName)



