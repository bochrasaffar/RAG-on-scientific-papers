from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

def parse_pdf(pdf_file_path):
  reader = PdfReader(pdf_file_path)
  text = ""
  for page in reader.pages:
      text += page.extract_text() + "\n"
  return text

def get_chunks_pdf(pdf_file_path):
  text = parse_pdf(pdf_file_path)
  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=60,
    length_function=len,
    is_separator_regex=False,
  )
  metadata = {"source": pdf_file_path}
  texts = text_splitter.create_documents([text])
  for t in texts:
    t.metadata = metadata
    t.page_content = t.page_content.replace('\\n','')
    t.page_content = t.page_content.replace('\n','')
    t.page_content = t.page_content.replace('\t','')
  return texts