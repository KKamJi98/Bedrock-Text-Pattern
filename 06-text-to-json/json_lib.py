import json
from json import JSONDecodeError
from langchain_community.chat_models import BedrockChat

# Bedrock LangChain 클라이언트를 생성하는 함수추가
def get_llm():

    model_kwargs =  { #Anthropic 모델
        "max_tokens": 8000, 
        "temperature": 0
        }
    
    llm = BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0", #파운데이션 모델 설정하기
        model_kwargs=model_kwargs) #Claude의 속성을 구성합니다.
    
    return llm  

# 텍스트 결과를 JSON 객체로 변환 시
def validate_and_return_json(response_text):
    try:
        response_json = json.loads(response_text) #텍스트를 JSON으로 로드하려고 시도합니다.
        return False, response_json, None #has_error, response_content, err을 반환합니다.
    
    except JSONDecodeError as err:
        return True, response_text, err #has_error, response_content, err을 반환합니다.

# Bedrock 호출 및 JSON 변환기에 응답 전달
def get_json_response(input_content): #text-to-text client 함수
    
    llm = get_llm()

    response = llm.invoke(input_content).content #프롬프트에 대한 텍스트 응답
    
    return validate_and_return_json(response)

