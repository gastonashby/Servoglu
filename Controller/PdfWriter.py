import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader, PdfFileWriter
from xhtml2pdf import pisa


def generateMetaData():
    # Generate PDF from a html file.
    with open('template.html', 'r') as myfile:
        data = myfile.read().replace('\n', '')

    resultFile = open('meta.pdf', "w+b")
    # convert HTML to PDF
    pisa.CreatePDF(data,dest=resultFile)
    # close output file
    resultFile.close()  # close output file

def generatePlots(results,xData,size,equations):
    with PdfPages('plots.pdf') as pdf:
        plt.figure(figsize=(8.27,11.69))
        i = 0
        for ec in equations:
            plt.plot(xData, results[:, i], label=ec.description.format(i=i))
            i+=1

        plt.legend(loc='best')
        plt.title('Model Equations')
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



def createPdf(results,xData,size,equations,fileName,pdfTuple):
    generateMetaData()
    generatePlots(results,xData,size,equations)
    mergePdfs(fileName)



