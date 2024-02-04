# Import necessary modules
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize ChatOpenAI instance
chat = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-3.5-turbo'
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

# add latest AI response to messages
messages.append(res)

# now create a new user prompt
prompt = HumanMessage(
    content="Can you tell me about the provisions in the 1987 Philippine Constitution?"
)
# add to messages
messages.append(prompt)

# send to OpenAI
res = chat(messages)

# Print or use the response as needed
print(res.content)