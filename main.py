from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st
from datetime import datetime
from utils import load_posts, save_posts, display_posts, get_user_country
from translations import translations
from css import custom_css

load_dotenv()
chat_model = ChatOpenAI()
PICKLE_FILE = 'posts.pkl'

def update_content():
    st.session_state.content = st.session_state.input
    st.session_state.button_clicked = True

# 초기 상태 설정
if 'content' not in st.session_state:
    st.session_state.content = ""
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False
if 'posts' not in st.session_state:
    st.session_state.posts = load_posts(PICKLE_FILE)
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = '인기 댓글순'
if 'language' not in st.session_state:
    # 사용자의 국가 정보를 기반으로 기본 언어 설정
    user_country = get_user_country()
    default_language = 'English'  # 기본 언어를 영어로 설정
    if user_country == 'KR':
        default_language = '한국어'
    elif user_country == 'CN':
        default_language = '中文'
    elif user_country == 'JP':
        default_language = '日本語'
    st.session_state.language = default_language

# CSS 스타일 적용
custom_css()

# HTML 및 CSS를 적용하여 타이틀과 입력 폼을 정의
st.markdown(f'<div class="main-title">{translations[st.session_state.language]["title"]}</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 입력 컨테이너
with st.container():
    content = st.text_input(translations[st.session_state.language]["prompt"], key='input', on_change=update_content)
    if st.session_state.button_clicked or st.button(translations[st.session_state.language]["submit"]):
        if st.session_state.content.strip() == "":
            st.warning(translations[st.session_state.language]["prompt"])
        else:
            st.write("input> ", content)
            prompt = (f"다음 문장을 꼬투리를 잡아 비꼬는 사람인 것처럼 답변해 주세요. "
                      f"말투도 나이든 사람이 젊은 사람에게 지적질 하는 말투여야 해요.: '{content}'\n"
                      f"답변을 생성하고 '쯧쯧쯧'으로 끝맺어 주세요."
                      f"비꼬는 답변:")
            with st.spinner('답변 작성 중...'):
                result = chat_model.invoke(prompt)
                st.write("output> ", result.content)
                new_post = {
                    "input": content,
                    "output": result.content,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "likes": 0,
                    "replies": []  # replies 항목은 유지하지만 기능은 사용하지 않음
                }
                st.session_state.posts.append(new_post)
                save_posts(st.session_state.posts, PICKLE_FILE)
            st.session_state.button_clicked = False

# 댓글 목록
st.write("---")
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1], gap="small")
with col1:
    st.markdown('<div class="subheader-container">', unsafe_allow_html=True)
    st.subheader(f"{len(st.session_state.posts)} {translations[st.session_state.language]['comments_title']}")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="sort-refresh-container">', unsafe_allow_html=True)
    sort_by_options = [translations[st.session_state.language]["sort_by_likes"], translations[st.session_state.language]["sort_by_recent"]]
    if st.session_state.sort_by not in sort_by_options:
        st.session_state.sort_by = sort_by_options[0]
    sort_by = st.selectbox("", sort_by_options, key='sort_by', label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 게시물 표시
display_posts(st.session_state.posts, st.session_state.sort_by, st.session_state.language, translations)

# Footer 추가
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <p>&copy; 2024 팀꾸루. All rights reserved.</p>
            <div class="language-select">
                <label for="language-select">Language: </label>
                <select id="language-select" onchange="window.location.href='?language=' + this.value;">
                    <option value="한국어" {selected_ko}>한국어</option>
                    <option value="English" {selected_en}>English</option>
                    <option value="中文" {selected_cn}>中文</option>
                    <option value="日本語" {selected_jp}>日本語</option>
                </select>
            </div>
        </div>
    </div>
    """.format(
    selected_ko='selected' if st.session_state.language == '한국어' else '',
    selected_en='selected' if st.session_state.language == 'English' else '',
    selected_cn='selected' if st.session_state.language == '中文' else '',
    selected_jp='selected' if st.session_state.language == '日本語' else ''
), unsafe_allow_html=True)
