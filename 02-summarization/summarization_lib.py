from langchain.prompts import PromptTemplate
from langchain_community.chat_models import BedrockChat
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def get_llm():
    
    model_kwargs =  { #Anthropic 모델
        "max_tokens": 8000, 
        "temperature": 0
        }
    
    llm = BedrockChat(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0", #파운데이션 모델 설정
        model_kwargs=model_kwargs) #Claude의 속성을 구성
    
    return llm

# 문서 청크 생성함수 추가
    # 해당 코드는 문서를 단락, 줄, 문장 또는 단어별로 분할 시도
pdf_path = "2022-Shareholder-Letter.pdf"

def get_docs():
    
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "], chunk_size=4000, chunk_overlap=100 
    )
    docs = text_splitter.split_documents(documents=documents)
    
    return docs

# Bedrock 호출
def get_summary(return_intermediate_steps=False):
    
    map_prompt_template = "{text}\n\n위의 내용을 Korean으로 bullet point 3개로 요약합니다:"
    map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])
    
    combine_prompt_template = "{text}\n\n위의 내용을 Korean으로 간결하게 bullet point 5개로 요약합니다:"
    combine_prompt = PromptTemplate(template=combine_prompt_template, input_variables=["text"])
    
    llm = get_llm()
    docs = get_docs()
    
    chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=map_prompt, combine_prompt=combine_prompt, return_intermediate_steps=return_intermediate_steps,verbose=True)
    
    if return_intermediate_steps:
        return chain.invoke({"input_documents": docs}, return_only_outputs=True)
    else:
        return chain.invoke(docs, return_only_outputs=True)

