""" 이 파일에서 해야 할 것:
  1. OllamaEmbeddings로 임베딩 모델 만들기 (모델명은 config.py에서)
  2. create_vectorstore(splits) 함수 — 문서 조각을 받아서 FAISS 벡터 저장소 생성 + 로컬에 저장
  3. load_vectorstore() 함수 — 저장된 벡터 저장소 불러오기
  4. 테스트 코드에서 loader.py의 load_and_split을 가져와서 벡터 저장소 생성
  """
# 벡터 저장소 생성/불러오기

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS  
from app.config import EMBEDDING_MODEL, VECTORSTORE_DIR


embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

def create_vectorstore(splits):
    vectorstore = FAISS.from_documents(splits, embeddings)
    vectorstore.save_local(VECTORSTORE_DIR)
    return vectorstore

def load_vectorstore():
    return FAISS.load_local(VECTORSTORE_DIR, 
                            embeddings,
                            allow_dangerous_deserialization=True # load_local()이 파일을 불러올 때 보안 확인을 하는 거, 불러오는 함수에 넣어야함
                            )


if __name__ == "__main__":
    from app.rag.loader import load_and_split

    splits =load_and_split("data/company_rules.txt")
    vectorstore = create_vectorstore(splits)
    print(f"벡터 저장소 생성 완료! 조각 수: {len(splits)}")