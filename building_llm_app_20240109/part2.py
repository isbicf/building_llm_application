#for PDF file we need to import PyPDFLoader from langchain framework
from langchain_community.document_loaders import PyPDFLoader

# for CSV file we need to import csv_loader
# for Doc we need to import UnstructuredWordDocumentLoader
# for Text document we need to import TextLoader

# filePath = "/content/A_miniature_version_of_the_course_can_be_found_here__1701743458.pdf"
filePath = "InSCight_2024.pdf"
loader = PyPDFLoader(filePath)
#Load document
pages = loader.load_and_split()
print(pages[1].page_content)
