import pandas as pd
from io import StringIO
from langchain_community.chat_models import BedrockChat

# Bedrock Langchain 클라이언트를 생성하는 함수를 추가
def get_llm():

    model_kwargs = {  # Anthropic 모델
        "max_tokens": 8000,
        "temperature": 0
    }

    llm = BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # 파운데이션 모델 설정
        model_kwargs=model_kwargs)  # Claude의 속성을 구성

    return llm

# 텍스트 결과를 판다스 데이터 프레임으로 변환하는 함수를 추가
    # 해당 과정을 통해 LLM이 유효한 CSV 형식의 텍스트를 생성하지 못하는 상황을 정상적으로 처리 가
def validate_and_return_csv(response_text):
    # has_error, response_content, err를 반환
    try:
        csv_io = StringIO(response_text)
        return False, pd.read_csv(csv_io), None  # 응답 CSV를 데이터 프레임에 로드하려고 시도

    except Exception as err:
        return True, response_text, err

# Bedrock을 호출 - 응답을 CSV 변환기로 전달
def get_csv_response(input_content):  # text-to-text 클라이언트 함수

    llm = get_llm()

    response = llm.invoke(input_content).content  # 프롬프트에 대한 텍스트 응답

    return validate_and_return_csv(response)
