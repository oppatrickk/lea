import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

load_dotenv()

class BertEmbeddings:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased')
        self.model = AutoModelForQuestionAnswering.from_pretrained('bert-large-uncased')
        self.model.eval()  # Make sure the model is in evaluation mode

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            if outputs.hidden_states is None:
                print("No hidden states found in the model output.")
                continue
            
            # Choose the appropriate layer from the hidden states
            hidden_states = outputs.hidden_states
            pooled_output = torch.cat((hidden_states[-1][:, 0, :], hidden_states[-1][:, -1, :]), dim=1)
            embeddings.append(pooled_output.squeeze().tolist())
        return embeddings

# ===========
# LOADER
# ===========

# Directory containing text files
path = './data/republic_acts/txt'

# Load and process text files
loader = DirectoryLoader(path, glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

# Splitting the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Instantiate the BertEmbeddings class
bert_embeddings = BertEmbeddings()

# Initialize Chroma with embeddings
persist_directory = 'db'
vectordb = Chroma.from_documents(
    documents=texts,
    embedding=bert_embeddings,
    persist_directory=persist_directory
)

# Persist the db to disk
vectordb.persist()
vectordb = None

# Load the persisted database from disk
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=bert_embeddings,
)

# Define retriever and LLM
retriever = vectordb.as_retriever(search_kwargs={"k": 2})
llm = bert_embeddings.model

# Create the question answering chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Cite sources
def process_llm_response(llm_response):
    print(llm_response['answer'])
    print('\n\nSources:')
    for source in llm_response["source_documents"]:
        print(source.metadata['source'])

query = "What is RA 9262?"
llm_response = qa_chain.invoke(query)
process_llm_response(llm_response)
