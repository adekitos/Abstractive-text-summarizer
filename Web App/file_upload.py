import streamlit as st
import streamlit.components.v1 as stc
import docx2txt
from PyPDF2 import PdfFileReader
import pdfplumber

def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text

def main():
    docx_file = " "
    docx_file = st.file_uploader("Upload File",type=['txt','docx','pdf'])
    raw_text= " "
    if (docx_file != None and docx_file != "" and docx_file !=" "):
        if st.button("Process"):
            file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
            st.write(file_details)
			# Check File Type
            if docx_file.type == "text/plain":
                    st.text(str(docx_file.read(),"utf-8")) 
                    raw_text = str(docx_file.read(),"utf-8") 
            elif docx_file.type == "application/pdf":
                   raw_text = read_pdf(docx_file)
					# st.write(raw_text)
                   try:
                       with pdfplumber.open(docx_file) as pdf:
                           page = pdf.pages[0]
                           st.write(page.extract_text())
                   except:
                               st.write("None")
				
            elif docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
				# Use the right file processor ( Docx,Docx2Text,etc)
                    raw_text = docx2txt.process(docx_file) # Parse in the uploadFile Class directory
                    #st.write(raw_text)
    
    return raw_text 

