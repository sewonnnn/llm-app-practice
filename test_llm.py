 # LLM 연결 테스트

from langchain_ollama import ChatOllama

model = ChatOllama(model="llama3")

result = model.invoke("안녕! 한국어로 짧게 자기소개 해줘.")
print(result.content)
