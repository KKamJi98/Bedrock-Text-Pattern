from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_models import BedrockChat
from langchain.chains import ConversationalRetrievalChain

from langchain_community.embeddings import BedrockEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Bedrock Langchain 클라이언트를 생성하는 함수를 추가합니다.

def get_llm():

    model_kwargs = {  # anthropic
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "temperature": 0
    }

    llm = BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # 파운데이션 모델 지정
        model_kwargs=model_kwargs)  # Claude 속성 구성

    return llm

# 인메모리 벡터 저장소를 생성하는 함수를 추가

def get_index():  # 애플리케이션에서 사용할 인메모리 벡터 저장소를 생성하고 반환합니다.

    embeddings = BedrockEmbeddings()  # Titan 임베딩 클라이언트를 생성합니다.

    pdf_path = "2022-Shareholder-Letter.pdf"  # 이 이름을 가진 로컬 PDF 파일을 가정합니다.

    loader = PyPDFLoader(file_path=pdf_path)  # PDF 파일 로드하기

    text_splitter = RecursiveCharacterTextSplitter(  # 텍스트 분할기 만들기
        # (1) 단락, (2) 줄, (3) 문장 또는 (4) 단어 순서로 청크를 분할합니다.
        separators=["\n\n", "\n", ".", " "],
        chunk_size=1000,  # 위의 구분 기호를 사용하여 1000자 청크로 나눕니다.
        chunk_overlap=100  # 이전 청크와 겹칠 수 있는 문자 수입니다.
    )

    index_creator = VectorstoreIndexCreator(  # 벡터 스토어 팩토리 만들기
        vectorstore_cls=FAISS,  # 데모 목적으로 인메모리 벡터 저장소를 사용합니다.
        embedding=embeddings,  # Titan 임베딩 사용
        text_splitter=text_splitter,  # 재귀적 텍스트 분할기 사용하기
    )

    # 로드된 PDF에서 벡터 스토어 인덱스를 생성합니다.
    index_from_loader = index_creator.from_loaders([loader])

    return index_from_loader  # 클라이언트 앱에서 캐시할 인덱스를 반환합니다.

# LangChain 메모리 객체 초기화 함수 추가
# ConversationBufferWindowMemory 클래스를 사용해 가장 최근 메시지를 추적하고 이전 메시지를 요약하여 긴 대화 동완 채팅 컨텍스트가 유지
def get_memory(): #이 채팅 세션을 위한 메모리 만들기
    
    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True) #이전 메시지의 기록을 유지합니다.
    
    return memory

# Bedrock 호출
# LangChain으로 Bedrock 클라이언트 생성 후 다음 입력 콘텐츠를 Bedrock으로 전달
def get_rag_chat_response(input_text, memory, index): #chat client 함수
    
    llm = get_llm()
    
    conversation_with_retrieval = ConversationalRetrievalChain.from_llm(llm, index.vectorstore.as_retriever(), memory=memory)
    
    chat_response = conversation_with_retrieval.invoke({"question": input_text}) #사용자 메시지, 기록 및 지식을 모델에 전달합니다.
    
    return chat_response['answer']


