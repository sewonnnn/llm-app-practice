""" 이 파일에서 해야 할 것:

  1. @tool 데코레이터로 계산기 도구 만들기
  2. 함수 이름: calculator
  3. 파라미터: expression: str (예: "3500 * 12")
  4. docstring 꼭 작성 — AI가 이걸 읽고 도구를 쓸지 판단해
  5. 테스트 코드에서 직접 호출해보기
  """

from langchain_core.tools import tool

@tool
def calculator(expression: str):
       # 진짜 docstring = 큰따옴표 3개
      """수학 계산을 수행합니다. 예: '3500 * 12'"""
      try:
        result = eval(expression) # 문자열을 코드로 실행하는 파이썬 내장 함수(실무에서는 사용x 위험함)
        return str(result)
      except:
           return "계산할 수 없는 수식입니다."
      


if __name__ == "__main__":
      print(calculator.invoke("3500 * 12"))
      print(calculator.invoke("100 + 200"))