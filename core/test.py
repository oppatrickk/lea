from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Load the BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Create the HuggingFacePipeline
pipeline = HuggingFacePipeline(model=model, tokenizer=tokenizer)

# Define the context and question
context = "The capital of France is Paris. It is a beautiful city with many landmarks such as the Eiffel Tower and the Louvre Museum."
question = "What is the capital of France?"

# Get the answer from the pipeline
result = pipeline({"question": question, "context": context})
print(result["answer"])