import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader, PdfFileWriter
from xhtml2pdf import pisa
import math


def generateMetaData(pdfTuple):
    # Generate PDF from a html file.
    with open('template.html', 'r') as myfile:
        html = myfile.read().replace('\n', '')

    htmlVariables = replaceVariables(html,pdfTuple)
    resultFile = open('meta.pdf', "w+b")
    # convert HTML to PDF
    pisa.CreatePDF(htmlVariables,dest=resultFile)
    # close output file
    resultFile.close()  # close output file

def replaceVariables(html,pdfTuple):
    html = html.replace("{{patientName}}",pdfTuple.patientName)
    html = html.replace("{{sex}}", pdfTuple.sex)
    html = html.replace("{{birthdate}}", pdfTuple.birthdate)
    html = html.replace("{{patientAdditionalInfo}}", pdfTuple.patientAdditionalInfo)
    html = html.replace("{{technician}}", pdfTuple.technician)
    html = html.replace("{{simulationInfo}}", pdfTuple.simulationInfo)
    html = html.replace("{{date}}", datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
    html = html.replace("{{modelInfo}}",pdfTuple.modelInfo)
    return html

def generatePlots(results,treatment,xData,size,equations,plotsPerPage):
    plotSize = math.ceil(xData.size / plotsPerPage)
    grid_size = (plotsPerPage, 1)

    with PdfPages('plots.pdf') as pdf:
        plt.figure(figsize=(8.27,8.27))

        plt.title('Model Equations')
        for i in range(0,plotsPerPage):
            plt.subplot2grid(grid_size, (i % plotsPerPage, 0))
            j = 0
            if i < plotsPerPage:
                for ec in equations:
                    plt.plot(xData[i*plotSize:(plotSize*(i+1))+1], results[i*plotSize:(plotSize*(i+1))+1, j], label=ec.description.format(i=j))
                    j+=1
            else:
                for ec in equations:
                    plt.plot(xData[i*plotSize:], results[i*plotSize:, j], label=ec.description.format(i=j))
                    j+=1
            plt.legend(loc=2, prop={'size': 6})


            # i = 0
            # plt.subplot2grid(grid_size, (1 % plotsPerPage, 0))
            # for ec in equations:
            #     plt.plot(xData[plotSize:(plotSize*2+1)], results[plotSize:(plotSize*2+1), i], label=ec.description.format(i=i))
            #     i+=1
            # plt.legend(loc=2, prop={'size': 6})
            #
            # #if last size - (plotsPerPage * plotSize)
            # i = 0
            # plt.subplot2grid(grid_size, (2 % plotsPerPage, 0))
            # for ec in equations:
            #     plt.plot(xData[plotSize*2:], results[plotSize*2:, i], label=ec.description.format(i=i))
            #     i += 1
            # plt.legend(loc=2, prop={'size': 6})

        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

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



def createPdf(results,treatment,xData,size,equations,fileName,pdfTuple,plotsPerPage):
    generateMetaData(pdfTuple)
    generatePlots(results,treatment,size,equations,plotsPerPage)
    mergePdfs(fileName)



