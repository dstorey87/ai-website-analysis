from llama3_vision_llm import Llama3VisionLLM

# Initialize the custom LLM wrapper
llama_llm = Llama3VisionLLM()

# Define a test prompt
prompt = "Describe the potential applications of AI vision models."

# Generate a response using the `invoke` method
response = llama_llm.invoke(prompt)
print("Llama 3.2 Vision Response:")
print(response)
