import datetime
import numpy
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader, PdfFileWriter
from xhtml2pdf import pisa
import math
import locale



def generateMetaData(pdfTuple,equations,constants):
    # Generate PDF from a html file.
    with open('template.html', 'r') as myfile:
        html = myfile.read().replace('\n', '')

    equationsDescription = "<strong>Equations:</strong> </br>"
    for e in equations:
        equationsDescription+= e.name + " = " + e.equation + "</br>"

    constantsDescription = "<strong>Constants:</strong> </br>"
    for c in constants:
        constantsDescription += c.name + " : " + c.value1 + " = " + c.value2 +"</br>"

    htmlVariables = replaceVariables(html,pdfTuple,equationsDescription,constantsDescription)
    resultFile = open('meta.pdf', "w+b")

    # convert HTML to PDF
    pisa.CreatePDF(htmlVariables,dest=resultFile)
    # close output file
    resultFile.close()  # close output file


def replaceVariables(html,pdfTuple,equationsDescription,constantsDescription):
    html = html.replace("{{patientName}}",pdfTuple.patientName)
    html = html.replace("{{sex}}", pdfTuple.sex)
    html = html.replace("{{birthdate}}", pdfTuple.birthdate)
    html = html.replace("{{patientAdditionalInfo}}", pdfTuple.patientAdditionalInfo)
    html = html.replace("{{technician}}", pdfTuple.technician)
    html = html.replace("{{simulationInfo}}", pdfTuple.simulationInfo)
    #Seteamos fecha en idioma local
    locale.setlocale(locale.LC_TIME, '')
    html = html.replace("{{date}}", datetime.datetime.now().strftime("%I:%M%p de %B %d, %Y"))
    html = html.replace("{{modelInfo}}",pdfTuple.modelInfo)
    html = html.replace("{{equations}}",equationsDescription)
    html = html.replace("{{constants}}", constantsDescription)
    return html

def generatePlotsWithTreatment(results,treatment,xData,size,equations,userDefined,plotSections,plotsPerPage,timeUnit):

    numberOfPages = math.ceil((plotSections * 2) / plotsPerPage)
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
            if i < plotSections:
                for ec in equations:
                    plt.plot(xData[i*plotSize:(plotSize*(i+1))+1], results[i*plotSize:(plotSize*(i+1))+1, j], label=ec.description + " (" + ec.unit + ")")
                    j+=1
            else:
                for ec in equations:
                    plt.plot(xData[i*plotSize:], results[i*plotSize:, j], label=ec.description + " (" + ec.unit + ")")
                    j+=1
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel("time"+"("+timeUnit+")") #TODO agregar unidad de tiempo en ejes y labels

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
                equationsIndex = 1

            h =0
            plt.subplot2grid(grid_size, (treatmentsIndex,0))
            for u in userDefined:
                plt.plot(xData[i * plotSize:(plotSize * (i + 1)) + 1],
                         treatment[i * plotSize:(plotSize * (i + 1)) + 1, h], label=u.description + " (" + u.unit + ")")
                h += 1
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel("time" + "(" + timeUnit + ")")
            plt.title('Simulated treatment')
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

def generatePlots(results,xData,size,equations,plotSections,plotsPerPage,timeUnit):

    numberOfPages = math.ceil((plotSections * 2) / plotsPerPage)
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
            if i < plotSections:
                for ec in equations:
                    plt.plot(xData[i*plotSize:(plotSize*(i+1))+1], results[i*plotSize:(plotSize*(i+1))+1, j], label=ec.description + " (" + ec.unit + ")")
                    j+=1
            else:
                for ec in equations:
                    plt.plot(xData[i*plotSize:], results[i*plotSize:, j], label=ec.description + " (" + ec.unit + ")")
                    j+=1
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel("time" + "(" + timeUnit + ")")
            plt.title('Model Equations')

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

def plotEquations(i,plotSections,equations,xData,plotSize,results):
    j = 0
    fig = None
    if i < plotSections:
        for ec in equations:
            fig = plt.figure(xData[i * plotSize:(plotSize * (i + 1)) + 1],
                     results[i * plotSize:(plotSize * (i + 1)) + 1, j], label=ec.description.format(i=j))
            j += 1
    else:
        for ec in equations:
            fig = plt.figure(xData[i * plotSize:], results[i * plotSize:, j], label=ec.description.format(i=j))
            j += 1
    fig.legend(loc=2, prop={'size': 6})
    return fig



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



def createPdf(results,treatment,xData,size,equations,userDefined,constants,fileName,pdfTuple,plotSections,plotsPerPage,timeUnit):

    generateMetaData(pdfTuple,equations,constants)
    if (len(treatment) > 0):
        generatePlotsWithTreatment(results, treatment, xData, size, equations, userDefined, plotSections, plotsPerPage,timeUnit)
    else:
        generatePlots(results, xData, size, equations, plotSections, plotsPerPage, timeUnit)
    mergePdfs(fileName)



