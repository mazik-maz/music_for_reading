# import PyPDF2
# from ebooklib import epub
# from bs4 import BeautifulSoup

# def extract_text_from_pdf(file):
#     reader = PyPDF2.PdfReader(file)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text

# def extract_text_from_epub(file):
#     book = epub.read_epub(file)
#     text = ''
#     for item in book.get_items():
#         if item.get_type() == ebooklib.ITEM_DOCUMENT:
#             soup = BeautifulSoup(item.get_content(), 'html.parser')
#             text += soup.get_text()
#     return text

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

