import PyPDF2
import docx
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_pdf(file_path):

    text=""

    with open(file_path,"rb") as file:

        reader=PyPDF2.PdfReader(file)

        for page in reader.pages:

            page_text=page.extract_text()

            if page_text:
                text+=page_text

    if text.strip()=="":
        images=convert_from_path(file_path)

        for img in images:
            text+=pytesseract.image_to_string(img)

    return text


def extract_text_from_docx(file_path):

    doc=docx.Document(file_path)

    text="\n".join([para.text for para in doc.paragraphs])

    return text


def extract_text(file_path):

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    elif file_path.endswith(".txt"):

        with open(file_path,"r",encoding="utf-8") as f:
            return f.read()

    else:
        return ""