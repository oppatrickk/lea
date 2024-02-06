# Import necessary modules
import os
import time
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from datasets import load_dataset
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone

# *
# * Chatbot
# *


load_dotenv() 

# Initialize ChatOpenAI instance
chat = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-3.5-turbo'
)

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Create a list of messages
messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?"),
    HumanMessage(content="What is the 1987 Philippine Constitution?.")
]

# Get the response from the chat model
res = chat(messages)

# Print or use the response as needed
print(res.content)

# # add latest AI response to messages
# messages.append(res)

# now create a new user prompt
# prompt = HumanMessage(
#     content="Can you tell me about the provisions in the 1987 Philippine Constitution?"
# )

# llmchain_information = [
#     "A LLMChain is the most common type of chain. It consists of a PromptTemplate, a model (either an LLM or a ChatModel), and an optional output parser. This chain takes multiple input variables, uses the PromptTemplate to format them into a prompt. It then passes that to the model. Finally, it uses the OutputParser (if provided) to parse the output of the LLM into a final format.",
#     "Chains is an incredibly generic concept which returns to a sequence of modular components (or other chains) combined in a particular way to accomplish a common use case.",
#     "LangChain is a framework for developing applications powered by language models. We believe that the most powerful and differentiated applications will not only call out to a language model via an api, but will also: (1) Be data-aware: connect a language model to other sources of data, (2) Be agentic: Allow a language model to interact with its environment. As such, the LangChain framework is designed with the objective in mind to enable those types of applications."
# ]

# source_knowledge = "\n".join(llmchain_information)

# query = "Can you tell me about the LLMChain in LangChain?"

# augmented_prompt = f"""Using the contexts below, answer the query.

# Contexts:
# {source_knowledge}

# Query: {query}"""

# # create a new user prompt
# prompt = HumanMessage(
#     content=augmented_prompt
# )
# # add to messages
# messages.append(prompt)

# # send to OpenAI
# res = chat(messages)

# print(res.content)



# # !
# # ! Server
# # !

# from pinecone import Pinecone

# # initialize connection to pinecone (get API key at app.pinecone.io)
# api_key = os.getenv("PINECONE_API_KEY") or "81741042-00ba-4f22-8697-e3f1158f0d83"

# # configure client
# pc = Pinecone(api_key=api_key)


# spec = ServerlessSpec(
#     cloud="aws", region="us-west-2"
# )

# index_name = 'llama-2-rag'
# existing_indexes = [
#     index_info["name"] for index_info in pc.list_indexes()
# ]

# # check if index already exists (it shouldn't if this is first time)
# if index_name not in existing_indexes:
#     # if does not exist, create index
#     pc.create_index(
#         index_name,
#         dimension=1536,  # dimensionality of ada 002
#         metric='dotproduct',
#         spec=spec
#     )
#     # wait for index to be initialized
#     while not pc.describe_index(index_name).status['ready']:
#         time.sleep(1)

# # connect to index
# index = pc.Index(index_name)
# time.sleep(1)
# # view index stats
# index.describe_index_stats()

# embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")

# texts = [
#     'this is the first chunk of text',
#     'then another second chunk of text is here'
# ]

# res = embed_model.embed_documents(texts)
# len(res), len(res[0])

# from tqdm.auto import tqdm  # for progress bar

# data = dataset.to_pandas()  # this makes it easier to iterate over the dataset

# batch_size = 100

# for i in tqdm(range(0, len(data), batch_size)):
#     i_end = min(len(data), i+batch_size)
#     # get batch of data
#     batch = data.iloc[i:i_end]
#     # generate unique ids for each chunk
#     ids = [f"{x['doi']}-{x['chunk-id']}" for i, x in batch.iterrows()]
#     # get text to embed
#     texts = [x['chunk'] for _, x in batch.iterrows()]
#     # embed text
#     embeds = embed_model.embed_documents(texts)
#     # get metadata to store in Pinecone
#     metadata = [
#         {'text': x['chunk'],
#          'source': x['source'],
#          'title': x['title']} for i, x in batch.iterrows()
#     ]
#     # add to Pinecone
#     index.upsert(vectors=zip(ids, embeds, metadata))

#     index.describe_index_stats()

# text_field = "text"  # the metadata field that contains our text

# # initialize the vector store object
# vectorstore = Pinecone(
#     index, embed_model.embed_query, text_field
# )

# query = "What is so special about Llama 2?"

# vectorstore.similarity_search(query, k=3)

# def augment_prompt(query: str):
#     # get top 3 results from knowledge base
#     results = vectorstore.similarity_search(query, k=3)
#     # get the text from the results
#     source_knowledge = "\n".join([x.page_content for x in results])
#     # feed into an augmented prompt
#     augmented_prompt = f"""Using the contexts below, answer the query.

#     Contexts:
#     {source_knowledge}

#     Query: {query}"""
#     return augmented_prompt

# print(augment_prompt(query))

# prompt = HumanMessage(
#     content=augment_prompt(
#         "what safety measures were used in the development of llama 2?"
#     )
# )
# res = chat(messages + [prompt])
# print(res.content)

# pc.delete_index(index_name)