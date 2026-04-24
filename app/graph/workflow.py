""" 해야 할 것:
  1. State 정의 — messages와 category 필드
  2. 노드 3개 만들기:
    - classify — 질문을 보고 refund, technical, general 중 하나로 분류
    - handle_refund — "환불 접수되었습니다. 3~5일 내 처리됩니다." 반환
    - handle_technical — "기술팀에서 확인 후 답변드리겠습니다." 반환
  3. 분기 함수 route — category에 따라 다른 노드로 보내기
  4. 그래프 조립 — StateGraph + 노드 추가 + 엣지 연결 + 컴파일
  """

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import LLM_MODEL

model = ChatOllama(model=LLM_MODEL)

  # 1. State 정의
class State(TypedDict):
      messages: Annotated[list, add_messages]
      category: str

  # 2. 노드: 질문 분류
def classify(state: State) -> dict:
      prompt = ChatPromptTemplate.from_template(
          "다음 문의를 분류해. refund, technical, general 중 하나만 답해: {q}"
      )
      chain = prompt | model | StrOutputParser()
      question = state["messages"][-1].content
      result = chain.invoke({"q": question})
      return {"category": result.strip()}

  # 3. 노드: 환불 처리
def handle_refund(state: State) -> dict:
       return {"messages": [{"role": "assistant", "content": "환불 접수되었습니다. 3~5일 내 처리됩니다."}]}


  # 4. 노드: 기술 문의
def handle_technical(state: State) -> dict:
      return {"messages": [{"role": "assistant", "content": "기술팀에서 확인 후 답변드리겠습니다."}]}

def handle_general(state: State) -> dict:
      return {"messages": [{"role": "assistant", "content": "일반 문의입니다. 빠른 답변 드리겠습니다."}]}

  # 5. 분기 함수
def route(state: State) -> str:
      # TODO: state["category"]에 따라 노드 이름 return
      if state["category"] in "refund":  #route에서는 'in' 사용
            return "handle_refund"
      elif state["category"] in "technical":
            return "handle_technical"
      else:
            return "handle_general"


  # 6. 그래프 조립
def create_workflow():
      graph = StateGraph(State) # 공동 칠판

      graph.add_node("classify",classify) # 카테고리 분류함수 넣기
      graph.add_node("handle_refund",handle_refund)
      graph.add_node("handle_technical",handle_technical) 
      graph.add_node("handle_general", handle_general)   # 노드 추가 
        
      # TODO: add_edge로 START → classify 연결

      graph.add_edge(START, "classify")

      # TODO: add_conditional_edges로 classify → route 연결
      graph.add_conditional_edges("classify", route)

      # TODO: add_edge로 각 처리 노드 → END 연결
      graph.add_edge("handle_refund", END)
      graph.add_edge("handle_technical", END)
      graph.add_edge("handle_general", END)
      return graph.compile()

if __name__ == "__main__":
    workflow = create_workflow()
    print(workflow.invoke({"messages": [{"role": "user", "content": "환불하고 싶어요"}]}))
    print(workflow.invoke({"messages": [{"role": "user", "content": "기술적인 문제를 해결해주세요"}]}))
    print(workflow.invoke({"messages": [{"role": "user", "content": "재고가 얼마나 남았나요?"}]}))