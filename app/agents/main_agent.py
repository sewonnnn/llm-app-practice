""" 이 파일에서 해야 할 것:
  1. ChatOllama 모델 불러오기
  2. calculator 도구 가져오기
  3. create_react_agent로 Agent 만들기
  4. create_agent() 함수로 감싸기
  5. 테스트 코드에서 2가지 질문 해보기:
    - 계산 질문: "3500 * 12는 얼마야?"
    - 일반 질문: "안녕하세요!

    +  main_agent.py를 수정해서 대화를 기억하는 Agent로 만들어줘. 

"""

# Agent + Memory

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from app.tools.calculator import calculator
from app.config import LLM_MODEL
from langgraph.checkpoint.memory import MemorySaver

def create_agent():
      model = ChatOllama(model=LLM_MODEL)
      checkpointer = MemorySaver()
      agent = create_react_agent(model, [calculator], checkpointer=checkpointer)  # 바로 담아도 됨
    #   calculator_tool = calculator
    #   agent = create_react_agent(model, [calculator_tool])
 
      return agent


if __name__ == "__main__":
      agent = create_agent()

    #   # 계산 질문
    #   result = agent.invoke(
    #       {"messages": [{"role": "user", "content": "3500 * 12는 얼마야?"}]}
    #   )
    #   print(result["messages"][-1].content)

    #   # 일반 질문
    #   result = agent.invoke(
    #       {"messages": [{"role": "user", "content": "안녕하세요!"}]}
    #   )
    #   print(result["messages"][-1].content)
      
      # invoke할 때 config 넣기
      config = {"configurable": {"thread_id": "test_123"}}

# 첫번째 질문
      result = agent.invoke(
      {"messages": [{"role": "user", "content": "내이름은 민수야"}]},
      config=config
  )
      print(result["messages"][-1].content)


# 두번째 질문
      result = agent.invoke(
      {"messages": [{"role": "user", "content": "내이름이 뭐라고 했지?"}]},
      config=config
  )
      print(result["messages"][-1].content)