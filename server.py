""" 해야 할 것:

  1. FastAPI 앱 만들기
  2. 2개 API 만들기:
    - POST /chat — Agent로 대화 (message, thread_id 받기)
    - POST /inquiry — Workflow로 고객 문의 분류 (message 받기)
  3. 요청 모델은 Pydantic BaseModel로 정의
  """

# FastAPI 서버

from fastapi import FastAPI
from pydantic import BaseModel
from app.agents.main_agent import create_agent
from app.graph.workflow import create_workflow

# 서버 시작 시 한번만 생성
app = FastAPI()
agent=create_agent()
workflow = create_workflow()

# API로 받을 데이터 형태를 정의
""" 
  프론트엔드에서 이런 JSON을 보냄
  {"message": "연차 며칠이야?", "thread_id": "abc-123"}
  이 JSON이 어떤 형태여야 하는지 정해주는 것.
"""
class ChatRequest(BaseModel):
      message: str
      thread_id: str

class InquiryRequest(BaseModel):
      message: str


@app.post("/chat")
def chat(request: ChatRequest): # ← 여기서 받음
   # 여기서는 invoke만
    config = {"configurable": {"thread_id": request.thread_id}} # 어떤 대화방인지 설정 (memory용)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config=config
    ) # agetn 실행: 도구 쓸지 판단 -> 답변 생성
    answer = result["messages"][-1].content # 대화 기록 중 마지막 메시지 꺼냄(최종 답변)
    return {"answer": answer} # 프론트에 json으로 응답



@app.post("/inquiry")
def inquiry(request: InquiryRequest):
    # → LangGraph 워크플로우 실행: 분류 → 분기 → 처리
    result = workflow.invoke(
         {"messages": [{"role": "user", "content": request.message}]}
         )
    answer = result["messages"][-1].content 

    return {"answer": answer, "category": result.get("category","")}
    # -> 최종 답변 + 분류 결과 같이 반환 / .get("category", "") = category 있으면 가져오고, 없으면 빈 문자열
