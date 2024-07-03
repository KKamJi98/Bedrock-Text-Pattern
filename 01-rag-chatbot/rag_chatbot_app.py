import streamlit as st 
import rag_chatbot_lib as glib

# 페이지의 제목, 구성 추가
st.set_page_config(page_title="RAG Chatbot") #HTML 제목
st.title("RAG Chatbot") #페이지 제목 

# 세션 캐시에 LangChain 메모리 추가
    # 해당 과정을 통해 사용자 세션당 고유한 채팅 메모리 유지 가능
    # Streamlit의 세션 상태를 서버 측에서 추적. 브라우저 탭이 닫히거나 애플리케이션이 중지되면 세션과 채팅 기록이 손실.
    # 실제 어플리케이션에서는 Amazon DynamoDB와 같은 데이터베이스에서 채팅 기록을 추적할 수 있음
if 'memory' not in st.session_state:
    st.session_state.memory = glib.get_memory()
    
# UI 채팅 기록을 세션 캐시에 추가
    # 해당 과정을 통해 사용자 상호작용이 있을 때마다 Streamlit 앱이 다시 실행될 때 채팅 기록을 UI에 다시 렌더링할 수 있음
    # 해당 과정이 없으면 새 채팅 메시지와 함께 이전 메시지가 사용자 인터페이스에서 사라짐
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
# 세션 캐시에 벡터 인덱스 추가
    # 해당 과정을 통해 사용자 세션당 인메모리 벡터 데이터베이스 유지 가능
if 'vector_index' not in st.session_state: #벡터 인덱스가 아직 생성되지 않았는지 확인
    with st.spinner("Indexing document..."): #이 블록의 코드가 실행되는 동안 스피너를 표시
        st.session_state.vector_index = glib.get_index() #지원 라이브러리를 통해 인덱스 검색 후 앱의 세션 캐시에 저장


# for 루프를 사용하여 이전 채팅 메시지를 렌더링
    # chat_history 세션 상태 개체를 기반으로 이전 메시지를 다시 렌더링
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])
        
# 입력 요소 추가
input_text = st.chat_input("당신의 봇과 여기서 대화하세요") #채팅 입력 상자를 표시합니다.

if input_text: #사용자가 채팅 메시지를 제출한 후 이 if 블록의 코드를 실행합니다.
    
    with st.chat_message("user"): #사용자 채팅 메시지를 표시합니다.
        st.markdown(input_text) #사용자의 최신 메시지를 렌더링합니다.
    
    st.session_state.chat_history.append({"role":"user", "text":input_text}) #사용자의 최신 메시지를 채팅 기록에 추가합니다.

    chat_response = glib.get_rag_chat_response(input_text=input_text, memory=st.session_state.memory, index=st.session_state.vector_index,) #지원 라이브러리를 통해 모델을 호출합니다.

    with st.chat_message("assistant"): #봇 채팅 메시지를 표시합니다.
        st.markdown(chat_response) #봇의 최신 답변을 표시합니다.
    
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #봇의 최신 메시지를 채팅 기록에 추가합니다.

