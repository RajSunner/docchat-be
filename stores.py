import os
import urllib.request
import PyPDF2
import io
from langchain.text_splitter import CharacterTextSplitter
import PyPDF2
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
from dotenv import load_dotenv
load_dotenv()

def create_vectors_from_url(url, name):
    req = urllib.request.Request(url)
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    reader = PyPDF2.PdfReader(remote_file_bytes)

    report_text = ''

    for x in range(len(reader.pages)):
      page = reader.pages[x]
      report_text += page.extract_text()

    report_splitter = CharacterTextSplitter(separator=" ",chunk_size=1000, chunk_overlap=100)
    texts = report_splitter.split_text(report_text)

    os.environ['OPENAI_API_KEY'] = os.environ['KEY']
    # Load Data to vectorstore
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts, embeddings)
    with open(name+".pkl", "wb") as f:
       pickle.dump(vectorstore, f)
    return vectorstore