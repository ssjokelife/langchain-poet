# from dotenv import load_dotenv
# load_dotenv()

from langchain_openai import ChatOpenAI, OpenAI

# llm = OpenAI()
# result = llm.invoke("내가 좋아하는 동물은 ")
# print(result)

# content = "14시간 근무하고 지금 퇴근해."

chat_model = ChatOpenAI()
# prompt = f"다음 문장을 초월적 긍정 사고(원영적사고)로 답변해 주세요: '{content}'\n긍정적 답변을 생성하고 '완전 럭키비키잔앙.'으로 끝맺어 주세요.\n긍정적 답변:"
# prompt = f"다음 문장에 대해 신입사원이 부장님에게 답변하는 말로"

# result = chat_model.invoke(prompt)
# print(result)

import streamlit as st

st.title('내 말을 들어줘.')
content = st.text_input("내용을 작성해 주세요.")
if st.button("말해줘."):
    st.write("input> ", content)
    prompt = (f"다음 문장을 꼬투리를 잡아 비꼬는 사람인 것처럼 답변해 주세요. "
              f"말투도 나이든 사람이 젊은 사람에게 지적질 하는 말투여야 해요.: '{content}'\n"
              f"답변을 생성하고 '쯧쯧쯧'으로 끝맺어 주세요."
              f"비꼬는 답변:")
    with st.spinner('답변 작성 중...'):
        result = chat_model.invoke(prompt)
        st.write("output> ", result.content)
