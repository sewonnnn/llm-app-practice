""" 이 파일에서 해야 할 것:                                                                                                                                                                                                                                     
  1. TextLoader로 txt 파일 불러오기                                                                                                                           
  2. RecursiveCharacterTextSplitter로 잘게 자르기 (chunk_size, chunk_overlap은 config.py에서 가져오기)                                                        
  3. load_and_split(file_path) 함수로 만들기                                                                                                                  
  4. 테스트 코드 추가해서 몇 개의 조각으로 나뉘는지 출력 
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP 


splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

#   함수 안에서 Loader를 만들어야함 그래야 파일 경로만 넘기면 동작
def load_and_split(file_path): # 경로 받아서
    loader = TextLoader(file_path) # 안에서 Loader 만들고
    docs = loader.load() # 로드하고
    return splitter.split_documents(docs) # 쪼개기

# 나중에 다른 파일도 쉽게 불러올 수 있음 load_and_split("data/다른문서.txt") ..등

if __name__ == "__main__":
    splits = load_and_split("data/company_rules.txt")
    print(f"조각 수: {len(splits)}") # 몇개의 조각이 벡터로 저장됐는지 확인
    print(f"첫 번째 조각: {splits[0].page_content}")