# 모델 설정
LLM_MODEL = "mistral"
EMBEDDING_MODEL = "nomic-embed-text" 

# RAG 설정
CHUNK_SIZE = 100  # 100자마다 쪼개기 500이라면-> 500자마다 쪼갬
CHUNK_OVERLAP = 50
RETRIEVER_K = 3

# 파일 경로
DATA_DIR = "data"
VECTORSTORE_DIR = "vectorstore_data"
