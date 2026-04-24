"""  이 파일에서 해야 할 것:

  1. ChatOllama 모델 불러오기 (model은 config.py에서 가져오기)
  2. ChatPromptTemplate 만들기 — {topic}을 받아서 "초등학생도 이해할 수 있게 설명해줘"라는 프롬프트
  3. StrOutputParser 연결
  4. | 파이프로 chain 만들기
  5. 맨 아래에 테스트 코드 추가
실행 방법: 
   cd ~/llm-app-practice
   source venv/bin/activate
   python -m app.chains.basic_chain
  """

# Prompt → Model → Parser 기본 체인

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import LLM_MODEL

model = ChatOllama(model=LLM_MODEL)

# from_messages — 여러 역할(system, user 등)을 나눠야 할 때 
"""                                                                                                
prompt = ChatPromptTemplate.from_messages([                                                                                                               
 ("system", "너는 친절한 선생님이야"),                                                                                                                   
 ("user", "{topic} 설명해줘")                                                                                                                          
])                                                                                                                                                          
"""
# from_template — 단순한 질문 하나일 때 
prompt = ChatPromptTemplate.from_template("{topic}에 대해 초등학생도 이해할 수 있게 설명해줘. 설명은 한국어로 해줘")

parser = StrOutputParser()

chain = prompt | model | parser

# 5. 테스트 코드
if __name__ == "__main__":
    result = chain.invoke({"topic": "헬로키티"})
    print(result)

