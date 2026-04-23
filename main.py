from ollama import chat
from ollama import ChatResponse

# Declares the list of AI models to be used and variable to store the value of the prompt
models = ["llama3", "deepseek-r1:1.5b", "mistral", "qwen3.5:4b"]
prompt = input("What shall the council debate? ")
# Declares the variables to store system prompts
system_prompt_llama3 = "You are a member of a council composed of 3 AI models, your role is to analyze the given prompt through a lens of neutrality"
system_prompt_deepseek = "You are a member of a council composed of 3 AI models, your role is to analyze the given prompt through the lens of scientific and technical analysis and give the most accurate results possible."
system_prompt_mistral = "You are a member of a council composed of 3 AI models, your role is to analyze the given prompt through the lens of pragmatism and provide the cleanest response"

def initial_questions(models, prompt, system_prompt_llama3, system_prompt_deepseek, system_prompt_mistral):
  response_llama: ChatResponse = chat(model=models[0], messages=[
    {
      'role': 'system','content': system_prompt_llama3,
      'role': 'user', 'content': prompt,
    },
  ])

  llama3_response_1 = response_llama['message']['content']

  response_deepseek: ChatResponse = chat(model = models[1], messages = [
    {
      'role': 'system', 'content': system_prompt_deepseek,
      'role': 'user', 'content': prompt,
    }
  ])

  deepseek_response_1 = response_deepseek['message']['content']

  response_mistral: ChatResponse = chat(model = models[2], messages= [
    {
      'role': 'system', 'content': system_prompt_mistral,
      'role': 'user', 'content': prompt, 
    }
  ])

  mistral_response_1 = response_mistral['message']['content']
  

  return(llama3_response_1, deepseek_response_1, mistral_response_1)

def vote(llama3_response_1, deepseek_response_1, mistral_response_1, system_prompt_deepseek, system_prompt_llama3, system_prompt_mistral):
  llama_vote: ChatResponse = chat(model = models[0], messages = [
    {
      'role': 'system', 'content': system_prompt_llama3, 
      'role': 'user', 'content': f"You will be provided with 2 responses, B and C, analyze them and vote which one is the best, reply with: The best option is followed by the letter of the response. Option B is {deepseek_response_1} and Option C is {mistral_response_1}"
    }
  ])
  llama_verdict = llama_vote['message']['content']

  deepsek_vote: ChatResponse = chat(model = models[1], messages = [
    {
      'role': 'system', 'content': system_prompt_deepseek,
      'role': 'user', 'content': f"You will be provided with 2 responses, A and C, analyze them and vote which one is the best, reply with: The best option is followed by the letter of the response. Option A is {llama3_response_1} and Option C is {mistral_response_1}"
    }
  ])
  deepseek_verdict = deepsek_vote['message']['content']
  
  mistral_vote: ChatResponse = chat(model = models[2], messages = [
    {
      'role': 'system', 'content': system_prompt_mistral,
      'role': 'user', 'content': f"You will be provided with 2 responses, A and B, analyze them and vote which one is the best, reply with: The best option is followed by the letter of the response. Option A is {llama3_response_1} and Option B is {deepseek_response_1}"
    }
  ])
  mistral_verdict = mistral_vote['message']['content']

  return(llama_verdict,deepseek_verdict,mistral_verdict)

def arbitrate(models, llama_verdict, deepseek_verdict, mistral_verdict, llama3_response_1, deepseek_response_1, mistral_response_1):
  qwen3_arbitrate: ChatResponse = chat(model = models[3], messages = [
    {
      'role': 'system', 'content': "You are an arbitrator for a council made up of 3 AI models. Your role is to judge their votes and determine the outcome with respect to their choices.",
      'role': 'user', 'content': f"These are the votes of the AI models: Llama3 (A) {llama_verdict}, DeepseekR1 (B) {deepseek_verdict}, Mistral (C) {mistral_verdict}. These are the original replies Llama3 {llama3_response_1}, DeepseekR1 {deepseek_response_1}, Mistral {mistral_response_1}, output only the prompt that wins the vote, alongside the voting score."
    }
  ])
  qwen_arbitration = qwen3_arbitrate['message']['content']
  return(qwen_arbitration)

llama3_response_1, deepseek_response_1, mistral_response_1 = initial_questions(models, prompt, system_prompt_llama3, system_prompt_deepseek, system_prompt_mistral)
llama_verdict, deepseek_verdict, mistral_verdict = vote(llama3_response_1, deepseek_response_1, mistral_response_1, system_prompt_deepseek, system_prompt_llama3, system_prompt_mistral)
result = arbitrate(models, llama_verdict, deepseek_verdict, mistral_verdict, llama3_response_1, deepseek_response_1, mistral_response_1)
print(result)