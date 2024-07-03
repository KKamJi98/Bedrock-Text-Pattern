import streamlit as st 
import json_lib as glib

st.set_page_config(page_title="Text에서 JSON 데이터 추출하기", layout="wide")  #열을 수용하기 위해 페이지 너비를 더 넓게 설정합니다.

st.title("Text에서 JSON 데이터 추출하기")  #페이지 제목

col1, col2 = st.columns(2)  #열 2개 생성

with col1: #이 with 블록의 모든 내용이 열 1에 배치됩니다.
    st.subheader("프롬프트") #이 열의 서브헤드
    
    input_text = st.text_area("텍스트 입력", height=500, label_visibility="collapsed")

    process_button = st.button("Run", type="primary") #기본 버튼 표시

with col2: #이 with 블록의 모든 내용이 열 2에 배치됩니다.
    st.subheader("결과") #이 열의 서브헤드
    
    if process_button: #버튼을 클릭하면 이 if 블록의 코드가 실행됩니다.
        with st.spinner("Running..."): #이 if 블록의 코드가 실행되는 동안 스피너를 표시합니다.
            has_error, response_content, err = glib.get_json_response(input_content=input_text) #지원 라이브러리를 통해 모델을 호출합니다.

        if not has_error:
            st.json(response_content) #오류가 없는 경우 JSON을 렌더링합니다.
        else:
            st.error(err) #그렇지 않으면 오류를 렌더링합니다.
            st.write(response_content) #그리고 모델의 원시 응답을 렌더링합니다.

