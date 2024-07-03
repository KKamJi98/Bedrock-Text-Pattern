import streamlit as st
import summarization_lib as glib

# 페이지 제목, 구성 추가
st.set_page_config(layout="wide", page_title="문서 요약")
st.title("문서 요약")

# 요약 요소 추가
return_intermediate_steps = st.checkbox("중간 단계 반환", value=True)
summarize_button = st.button("요약", type="primary")

if summarize_button:
    st.subheader("통합 요약")

    with st.spinner("Running..."):
        response_content = glib.get_summary(return_intermediate_steps=return_intermediate_steps)


    if return_intermediate_steps:

        st.write(response_content["output_text"])

        st.subheader("Section summaries")

        for step in response_content["intermediate_steps"]:
            st.write(step)
            st.markdown("---")

    else:
        st.write(response_content["output_text"])


