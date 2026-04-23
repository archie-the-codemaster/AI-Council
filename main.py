from ollama import chat
from ollama import ChatResponse

# Declares the list of AI models to be used
models = ["llama3", "deepseek-r1:1.5b", "mistral"]



response: ChatResponse = chat(model=models[1], messages=[
  {
    'role': 'user',
    'content': 'What are the best ways to avoid conflicts between nations',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)