
from langchain_ollama import ChatOllama
#base_url_model = os.getenv("BASE_URL_MODEL1")
base_url_model = 'http://10.8.0.11:11434'

llm = ChatOllama(model="gpt-oss:20b", base_url=base_url_model)


response = llm.invoke("Tell me a joke")

print(response)


