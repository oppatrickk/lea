from dotenv import load_dotenv
import os

# OpenAI GPT-3.5 API Key
load_dotenv() 
os.environ["OPENAI_API_KEY"]

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader

# Load and process the text files
path = './data/republic_acts/txt'
loader = DirectoryLoader(path, glob="**/*.txt", loader_cls=TextLoader)

documents = loader.load()
print("Files loaded: ", os.listdir(path))

# Splitting the text into
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

print(len(texts), "texts")