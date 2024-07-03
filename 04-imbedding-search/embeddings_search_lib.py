from langchain_community.embeddings import BedrockEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader

# 인메모리 벡터 저장소를 생성하는 함수 추가
def get_index(): #애플리케이션에서 사용할 인메모리 벡터 저장소를 생성하고 반환
    
    embeddings = BedrockEmbeddings() #Titan Embedding 클라이언트 생성하기
    
    loader = CSVLoader(file_path="sagemaker_answers.csv")

    index_creator = VectorstoreIndexCreator(
        vectorstore_cls=FAISS,
        embedding=embeddings,
        text_splitter=CharacterTextSplitter(chunk_size=300, chunk_overlap=0),
    )

    index_from_loader = index_creator.from_loaders([loader])
    
    return index_from_loader

# 사용자의 입력에 따라 이전에 생성된 인덱스를 검색하여 최적의 결과를 평탄화(flatten)한 형태로 반환
def get_similarity_search_results(index, question):
    results = index.vectorstore.similarity_search_with_score(question)
    
    flattened_results = [{"content":res[0].page_content, "score":res[1]} for res in results] #더 쉽게 표시하고 다룰 수 있도록 결과를 평탄화(flatten)
    
    return flattened_results

# 해당 함수를 추가하여 쿼리에 대한 원시 임베딩을 가져오는 함수 호출
def get_embedding(text):
    embeddings = BedrockEmbeddings() #Titan Embedding 클라이언트 생성
    
    return embeddings.embed_query(text)

