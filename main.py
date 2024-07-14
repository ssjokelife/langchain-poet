# from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import streamlit as st
from datetime import datetime
from utils import load_posts, save_posts, display_posts, get_user_country
from translations import translations
from css import custom_css

# load_dotenv()
chat_model = ChatOpenAI()
PICKLE_FILE = 'posts.pkl'

# 'Buy Me a Coffee' 버튼 HTML 및 CSS 코드
buy_me_a_coffee_button = """
<div style="position: fixed; bottom: 50px; right: 10px;">
    <a href="https://www.buymeacoffee.com/your_username" target="_blank">
        <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=your_username&button_colour=FFDD00&font_colour=000000&font_family=Arial&outline_colour=000000&coffee_colour=ffffff" />
    </a>
</div>
"""

description = """
내 말을 들어줘.는 가벼운 내용부터 마음의 깊은 고민들을 여러 관점으로 피드백을 얻기 위한 앱입니다.
세상에는 다양한 사람들이 있다 보니 같은 내용에 대해 어떤 경우는 위로를 받기도 하고 상처를 받기도 합니다.
최근 한국에서는 '원영적 사고'로 불리는 초월적 긍정 사고방식이 밈처럼 퍼졌었습니다.
우리도 '원영적 사고'를 통해 긍정적인 힘을 낼 수 있기를 바라며 언제나 화이팅 입니다.
"""


def update_content():
    st.session_state.content = st.session_state.input
    st.session_state.button_clicked = True


def set_language():
    lang = st.session_state.language_select
    st.session_state.language = lang
    st.query_params["language"] = lang


# 초기 상태 설정
if 'language' in st.query_params:
    st.session_state.language = st.query_params['language']
else:
    if 'language' not in st.session_state:
        user_country = get_user_country()
        default_language = 'English'  # 기본 언어를 영어로 설정
        if user_country == 'KR':
            default_language = '한국어'
        elif user_country == 'CN':
            default_language = '中文'
        elif user_country == 'JP':
            default_language = '日本語'
        st.session_state.language = default_language

if 'content' not in st.session_state:
    st.session_state.content = ""
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False
if 'posts' not in st.session_state:
    st.session_state.posts = load_posts(PICKLE_FILE)
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = '인기 댓글순'
if 'language_select' not in st.session_state:
    st.session_state.language_select = st.session_state.language

# CSS 스타일 적용
custom_css()

# 타이틀과 설명 힌트 추가
st.markdown(f'''
    <div class="main-title" title="{description}">
        <strong>{translations[st.session_state.language]["title"]}</strong>
        <br>
        <span style="font-size: 0.7em; color: #888;">(설명을 보려면 마우스를 올려보세요)</span>
    </div>
''', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 입력 컨테이너
with st.container():
    content = st.text_area(translations[st.session_state.language]["prompt"], key='input', on_change=update_content)
    if st.session_state.button_clicked or st.button(translations[st.session_state.language]["submit"]):
        if st.session_state.content.strip() == "":
            st.warning(translations[st.session_state.language]["prompt"])
        else:
            prompt_1 = (f"초월적 긍정 답변을 해주세요."
                        f"어떤 안좋은 내용도 결과적으로 좋게 해석해야 합니다."
                        f"답변을 생성하고 럭키쥐피티로 끝맺어 주세요."
                        f"긍정적 답변:")
            prompt_2 = (f"다음 문장을 꼬투리를 잡아 비꼬는 사람인 것처럼 답변해 주세요. "
                      f"말투도 나이든 사람이 젊은 사람에게 지적질 하는 말투여야 해요.: '{content}'\n"
                      # f"답변을 생성하고 '쯧쯧쯧'으로 끝맺어 주세요."
                      f"비꼬는 답변:")
            prompt_3 = (f"다음 문장을 듣긴 하지만 나랑 상관없는 것처럼 답변해 주세요."
                        f"20대 젊은 mz세대 말투면 좋겠습니다."
                        f"아. 넵! 과 같은 짧은 감탄사도 표현되면 좋아요."
                        f"상관없는 답변:")
            prompt_4 = (f"다음 문장을 듣고 엄마가 나에게 하는 잔소리로 만들어 주세요."
                        f"다 너를 위해서 하는 말이라는 뉘앙스가 포함되면 좋아요."
                        f"잔소리:")
            with st.spinner('답변 작성 중...'):
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                answer = ""
                result_1 = chat_model.invoke(prompt_1)
                print(result_1)
                answer += f"<p><strong>초긍정: </strong>{result_1.content}</p>"
                result_2 = chat_model.invoke(prompt_2)
                print(result_2)
                answer += f"<p><strong>비꼬는: </strong>{result_2.content}</p>"
                result_3 = chat_model.invoke(prompt_3)
                print(result_3)
                answer += f"<p><strong>상관없는: </strong>{result_3.content}</p>"
                result_4 = chat_model.invoke(prompt_4)
                print(result_4)
                answer += f"<p><strong>잔소리: </strong>{result_4.content}</p>"

                st.markdown(f"""
                        <div style="border: 1px solid #d3d3d3; padding: 10px; border-radius: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                            <p><strong>Input:</strong> {content}</p>
                            {answer}
                            <p style="color: #888888; font-size: 12px;">{now}</p>
                        </div>
                        """, unsafe_allow_html=True)
                new_post = {
                    "input": content,
                    "output": answer,
                    "timestamp": now,
                    "likes": 0,
                    "replies": []
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

# Footer와 언어 선택
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <p>&copy; 2024 팀꾸루. All rights reserved.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 언어 선택
language_options = ["한국어", "English", "中文", "日本語"]
# st.selectbox("Language:", language_options,
#              key='language_select',
#              index=language_options.index(st.session_state.language),
#              on_change=set_language,
#              label_visibility="collapsed")

# Footer의 언어 선택 부분에 Streamlit selectbox를 삽입
st.markdown(
    """
    <script>
        function moveSelectbox() {
            var container = document.querySelector('#language-select-container');
            var select = document.querySelector('select[data-baseweb="select"]');
            if (container && select) {
                container.appendChild(select.parentElement);
            }
        }
        setTimeout(moveSelectbox, 100);
    </script>
    """,
    unsafe_allow_html=True
)
