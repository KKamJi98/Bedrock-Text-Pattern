from langchain.chains import ConversationChain
from langchain_community.chat_models import BedrockChat

# 스트리밍 기능을 활성화한 코드를 추가하여 Boto3로 Bedrock 클라이언트를 생성
def get_llm(streaming_callback):
    model_kwargs = {
        "max_tokens": 4000,
        "temperature": 0
    }  # 데이터 추출의 경우, temperature가 낮을수록 좋습니다

    llm = BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",  # 파운데이션 모델 설정
        model_kwargs=model_kwargs,  # Claud에 대한 속성 구성
        streaming=True,
        callbacks=[streaming_callback],
    )
    return llm

# 스트리밍 호출 메서드를 사용하여 Bedrock을 호출
# 응답 청크가 반환되면 청크의 텍스트를 제공된 콜백 메서드에 전달
def get_streaming_response(prompt, streaming_callback):
    conversation_with_summary = ConversationChain(
        llm = get_llm(streaming_callback)
    )
    return conversation_with_summary.predict(input=prompt)

