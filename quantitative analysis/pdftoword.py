from docx import Document
import PyPDF2

FILE_PATH = 'C:/Users/skmid/OneDrive/Desktop/Resume/Good Example Resume.pdf'

document = Document()
with open(FILE_PATH, mode='rb') as f:

    reader = PyPDF2.PdfReader(f)

    page = reader.pages[0]

    print(page.extract_text())
    document.add_paragraph(page.extract_text())

    document.save('C:/Users/skmid/OneDrive/Desktop/Resume/output.docx')

