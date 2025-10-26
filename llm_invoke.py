"""
llm_invoke.py

"""

from langchain_groq import ChatGroq

# llama-3.3-70b-versatile

llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    temperature=0.5
)

x = llm.invoke("Cuéntame un chiste sobre bombillas!")

print()
print(type(x))
print()
print(x)