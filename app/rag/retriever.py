""" 1. load_vectorstore()로 저장된 벡터 불러오기                                                                                                                               
  2. retriever 만들기 (k값은 config.py에서)
  3. RAG chain 만들기 — 검색 결과 + 질문 → LLM 답변
  4. 테스트: "연차 며칠이야?" 질문해보기
  """

# 검색 + RAG 체인

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.rag.vectorstore import load_vectorstore
from app.config import LLM_MODEL, RETRIEVER_K

 # 벡터 불러오기 및 retriever 만들기
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K}) # retriever → 질문을 받아서 → 관련 문서를 검색해서 넘김

  # 프롬프트 — 검색된 문서를 참고해서 답변하라고 지시
prompt = ChatPromptTemplate.from_template("""
  아래 문서를 참고해서 질문에 답변해줘.
  문서에 없는 내용이면 "모르겠습니다"라고 답해줘.

  [참고 문서]
  {context}

  [질문]
  {question}
  """)

model = ChatOllama(model=LLM_MODEL)

parsers = StrOutputParser()

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | parsers
)
#   RunnablePassthrough → 질문을 받아서 → 그대로 넘김

if __name__ == "__main__":
    result= chain.invoke("사내 동호회 종류가 뭐야?") # 문자열 하나만 넘기면 됨 
    print(result)
"""  
 "연차 며칠이야?" 라는 문자열이 들어오면:
  retriever          → "연차 며칠이야?"로 문서 검색 → context에 넣음
  RunnablePassthrough → "연차 며칠이야?" 그대로     → question에 넣음
"""
   