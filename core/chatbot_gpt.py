import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

## OpenAI GPT-3.5 API Key
load_dotenv() 
os.environ["OPENAI_API_KEY"]

# ===========
# LOADER
# ===========

file_type = "txt"

# Load and process the text files
if file_type == "txt":
    path = './data/republic_acts/txt'
    glob = "**/*.txt"

elif file_type == "json":
    path = './data/republic_acts/json'
    glob = "**/*.json"

loader = DirectoryLoader(
    path, 
    glob = glob,
    loader_cls = TextLoader
    )

documents = loader.load()
print(len(documents), "Files loaded: ", os.listdir(path))

# Splitting the text into
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=0,
    )

texts = text_splitter.split_documents(documents)

# TODO: Use \n separator

print(len(texts), "texts")

# =========
# Loader
# =========

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk

embedding_model = 1; 
# 1 = OpenAI
# 2 = HuggingFace (multi-qa-MiniLM-L6-dot-v1)
# 3 = HuggingFace (paraphrade-multilingual-MiniLM-L12-v2)

if embedding_model == 1:
    embedding = OpenAIEmbeddings()
    persist_directory = 'data/database/openai'
    
elif embedding_model == 2:
    huggingface_model="sentence-transformers/multi-qa-MiniLM-L6-dot-v1"
    persist_directory = 'data/database/huggingface/multi-qa-MiniLM-L6-dot-v1'

elif embedding_model == 3:
    huggingface_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    persist_directory = 'data/database/huggingface/paraphrase-multilingual-MiniLM-L12-v2'

if embedding_model == 2 or embedding_model == 3: 
    embedding = HuggingFaceEmbeddings(
    model_name =huggingface_model,
    model_kwargs = {"device": "cpu", "trust_remote_code": True},
    encode_kwargs = {"normalize_embeddings": False,}
    )

# Embeddings Comparison
# https://www.sbert.net/docs/pretrained_models.html

# =========
# ChromaDB
# =========

vectordb = Chroma.from_documents(
    documents=texts, 
    embedding=embedding,
    persist_directory=persist_directory
    )

# persist the db to disk
vectordb.persist()
vectordb = None

# Now we can load the persisted database from disk, and use it as normal. 
vectordb = Chroma(
    persist_directory=persist_directory, 
    embedding_function=embedding
    )

retriever = vectordb.as_retriever()
retriever = vectordb.as_retriever(search_kwargs={"k": 2}) # k = number of documents to return

# Set up the turbo LLM
turbo_llm = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo'
)

# create the chain to answer questions 
qa_chain = RetrievalQA.from_chain_type(
    llm=turbo_llm, 
    chain_type="stuff", 
    retriever=retriever, 
    return_source_documents=True
    )

# Conversational
# https://towardsdatascience.com/4-ways-of-question-answering-in-langchain-188c6707cc5a

## Cite sources
def process_llm_response(llm_response):
    print(llm_response['result'])
    print('\n\nSources:')
    for source in llm_response["source_documents"]:
        print(source.metadata['source'])

query = "What is section 10 of RA 9262?"
llm_response = qa_chain.invoke(query)
process_llm_response(llm_response)